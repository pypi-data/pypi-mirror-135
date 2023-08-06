from setuptools import setup, find_packages


def read_file(file):
	with open(file, "r") as fh:
		return fh.read()


setup(
	name="dexscreener",
	packages=find_packages(),
	version="0.0.1",
	license="MIT",

	description="Python wrapper for the 'dexscreener.com' API",
	long_description=read_file("README.md"),
	long_description_content_type="text/markdown",

	author="Joshua Nixon",
	author_email="joshuanixonofficial@gmail.com",

	url="https://github.com/nixonjoshua98/dexscreener",

	download_url="https://github.com/nixonjoshua98/dexscreener/archive/refs/tags/0.0.1.tar.gz",

	keywords=[
		"dexscreener",
		"crypto",
		"cryptocurrency"
	],

	install_requires=[
		"requests",
		"pydantic",
		"certifi"
	],

	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"Topic :: Software Development :: Build Tools",
	],

	python_requires='>=3.9'
)
