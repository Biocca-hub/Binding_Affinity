import argparse
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from itertools import combinations
from pathlib import Path


FORMAT_OUTPUT = "query,target,alntmscore,qcov,qtmscore,tcov,ttmscore"


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description="Run all-vs-all unordered foldseek easy-search over PDB files in a directory."
	)
	parser.add_argument("directory", help="Directory containing .pdb files")
	parser.add_argument("num_workers", type=int, help="Maximum parallel foldseek jobs")
	return parser.parse_args()


def run_foldseek(file1: Path, file2: Path, out_file: Path, tmp_dir: Path) -> subprocess.CompletedProcess:
	cmd = [
		"foldseek",
		"easy-search",
		str(file1),
		str(file2),
		str(out_file),
		str(tmp_dir),
		"--alignment-type",
		"1",
		"--prefilter-mode",
		"2",
		"--format-output",
		FORMAT_OUTPUT,
	]
	return subprocess.run(cmd, capture_output=True, text=True)


def main() -> int:
	args = parse_args()

	if args.num_workers < 1:
		raise SystemExit("num_workers must be >= 1")

	directory = Path(args.directory)
	if not directory.is_dir():
		raise SystemExit(f"Directory not found: {directory}")

	pdb_files = sorted(path for path in directory.iterdir() if path.is_file() and path.suffix == ".pdb")

	if len(pdb_files) < 2:
		raise SystemExit("Need at least two .pdb files in the directory")

	tmp_root = Path.cwd() / "tmp"
	if tmp_root.exists():
		raise SystemExit(f"Temporary directory already exists: {tmp_root}")
	tmp_root.mkdir()

	jobs = []
	for index, (file1, file2) in enumerate(combinations(pdb_files, 2), start=1):
		out_file = tmp_root / f"{file1.stem}_{file2.stem}_out.tsv"
		tmp_dir = tmp_root / f"tmp-{index}"
		tmp_dir.mkdir()
		jobs.append((file1, file2, out_file, tmp_dir))

	try:
		failures = []
		with ThreadPoolExecutor(max_workers=args.num_workers) as executor:
			futures = [
				executor.submit(run_foldseek, file1, file2, out_file, tmp_dir)
				for file1, file2, out_file, tmp_dir in jobs
			]
			for (file1, file2, _, _), future in zip(jobs, futures):
				result = future.result()
				if result.returncode != 0:
					failures.append((file1.name, file2.name, result.stderr.strip()))

		if failures:
			for name1, name2, stderr in failures:
				print(f"foldseek failed for {name1} vs {name2}")
				if stderr:
					print(stderr)
			return 1

		merged_out = Path.cwd() / "out.tsv"
		with merged_out.open("w", encoding="utf-8") as fout:
			for _, _, out_file, _ in jobs:
				if out_file.exists():
					with out_file.open("r", encoding="utf-8") as fin:
						fout.write(fin.read())

		return 0
	finally:
		if tmp_root.exists():
			shutil.rmtree(tmp_root)


if __name__ == "__main__":
	raise SystemExit(main())
