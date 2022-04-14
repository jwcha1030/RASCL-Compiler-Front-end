int a;
int b;
int bignum;
int sqr;
float avg;
int numbers[5];


function int square(int num) {
    return num * num;
}

function float average(int nums[], int length) {
    int index;
    float sum;

    sum = 0.0;
    index = 0;
    while (index < length) {
       sum = sum + square(nums[index]);
    }
        
    return sum / length;
}

{
  numbers[0] = 50;
  numbers[1] = 52;
  numbers[2] = 12;
  numbers[3] = 31;
  numbers[4] = -17;
  float avg = average(numbers, 5);
  print avg;
}
