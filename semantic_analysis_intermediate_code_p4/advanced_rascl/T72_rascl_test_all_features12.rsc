int a;
int b;
int bignum;
int sqr;
float avg;
int numbers[5];


function void outputArray(int nums[], int length) {
    int index;
    index = 0;
    while (index < length) {
       print(nums[index]);
   }
}

function int max(int nums[], int length) {
    int largest;
    int index;
    largest = nums[0];
    index = 1;    

    while (index < length) {
       if (nums[index] > largest) {
          largest = nums[index];
       }
    }
        
    return largest;
}

{
  numbers[0] = 50;
  numbers[1] = 52;
  numbers[2] = 12;
  numbers[3] = 31;
  numbers[4] = -17;
  outputArray(numbers, 5);
  avg = average(numbers, 5);
  print avg;
}
