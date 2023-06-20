{
  imports = [
    ./packages
  ];

  perSystem = {pkgs, ...}: {
    formatter = pkgs.alejandra;
  };
}
