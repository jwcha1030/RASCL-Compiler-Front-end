float a;
int b, c;
int d[5];

{
  a = 5.;
  b = 1;
  if (a == b)
  {
    d[a] = 5;
    c = a + -b;
  }
  else
  {
    while (b < 5) {
        c = -a * b;
	b = b + 1;
    };
  };
  print c;
}
