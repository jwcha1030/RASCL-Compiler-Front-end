int a;
int b;
int bignum;
int sqr;
function int square(int num) {
 return num * num;
}
function int dude(int a, int b) {
 int theSum;
 theSum = a * a + b * b;
 return theSum;
}
{
 a = 5;
 b = 10;
 sqr = square(a);
 bignum = dude(a, b);
 print sqr;
 print bignum;
}
