with import <nixpkgs> { };

let
  pythonPackages = python3Packages;
in pkgs.mkShell {
  buildInputs = [
    pythonPackages.python

    pythonPackages.pip
    pythonPackages.setuptools
    pythonPackages.pandas
    pythonPackages.openpyxl
    pythonPackages.twine

    pre-commit
    yt-dlp
    ffmpeg
  ];

}
