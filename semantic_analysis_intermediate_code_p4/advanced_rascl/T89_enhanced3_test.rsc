int a;
int b;
int bignum;
int sqr;
float avg;
int numbers[5][5];
int even;
int index;


function int isEven (int val) {
    float joe[10][3];
    if (val == 0) {
       return 1;
    } else {
      if (val == 1) {
       return 0;
       } else {
          return isEven(val - 2);
       }
    }
}

{
  index = 0;
  even = 0;

  bignum = 5;
  b = 7;
  a = 2;
  
  ind1 = 0;  
  ind2 = 0;
  while (ind1 < 5) {
     if (bignum < b) && (a > 0) {
      	print numbers[0][ind1];
     } else {
	print numbers[1][ind1] - numbers[0][ind1];
     };
     ind1 = ind1 + 1;
     if (isEven(ind1)) {
        print ind1;
     };
     b = b * -1;
  }

}
