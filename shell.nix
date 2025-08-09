with import <nixpkgs> {};
pkgs.mkShell {
  packages = with pkgs; [
    (python3.withPackages(p: with p; [
      build
      pydantic
      sphinx
      sphinxemoji
      (
        buildPythonPackage rec {
          pname = "sphinx_press_theme";
          version = "0.9.1";
          src = fetchPypi {
            inherit pname version;
            sha256 = "sha256-FkPe5zZfeDHR05cbOJt8JVZBp6ztdfBoH3FXTjgARs8=";
          };
          pyproject = true;
          build-system = [ setuptools ];
          doCheck = false;
          dependencies = [ sphinx ];
        }
      )
      twine
    ]))
  ];
}
