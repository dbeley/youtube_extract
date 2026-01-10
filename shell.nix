{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python313
    python313Packages.pip
    python313Packages.virtualenv
    python313Packages.openpyxl
    python313Packages.pandas
    python313Packages.pytest

    yt-dlp
    ffmpeg
    prek
  ];
}
