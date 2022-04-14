float principle;
float rate;
int period;
float payment;

{
  principle = 300000.0;
  rate = 4.5;
  period = 360;

  payment = principle * (1+rate)/(1+rate)-1;    

  print payment;
}
