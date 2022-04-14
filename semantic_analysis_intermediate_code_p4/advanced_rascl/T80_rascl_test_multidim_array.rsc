int a;
int b;
int bignum;
int sqr;
float avg;
int numbers[5][5];
int even;
int index;


function int isEven (int val) {
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

  numbers[0][0] = 50;
  numbers[0][1] = -52;
  numbers[0][2] = -12;
  numbers[0][3] = 31;
  numbers[0][4] = -17;
  numbers[1][0] = 50;
  numbers[1][1] = -31;
  numbers[1][2] = 12;
  numbers[1][3] = 31;
  numbers[1][4] = 5;

  ind1 = 0;  
  ind2 = 0;
  while (ind1 < 5) {
     if (numbers[0][ind1] == numbers[1][ind1]) {
     	print numbers[0][ind1];
     } else {
	print numbers[1][ind1] - numbers[0][ind1];
     }
     ind1 = ind1 + 1;
     if (isEven(ind1)) {
        print ind1;
     }
  }

}
