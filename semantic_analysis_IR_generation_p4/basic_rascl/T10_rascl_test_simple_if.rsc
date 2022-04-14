int a[5], b;
float c, d[4];
{
  a[2] = 5;
  a[3] = 10;
  b = a[2] + a[3] * 2;
  while (b > 0)
  {
    print b;
    if (b < 10)
    {
       b = b - 1;
    }
    else
    {
       b = b - 2;
    };
  };
  print a[2];
}
