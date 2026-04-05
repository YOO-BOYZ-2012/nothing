import java.util.Scanner;
import java.util.Random;
public class numguess {
    public static void main(String[] args) {
        Scanner pain = new Scanner(System.in);
        Random random = new Random();
        int numtbg = random.nextInt(1, 101);
        int num;
        int attempt=0;
        do {
            System.out.print(" enter a number between 1-100:");
            num = pain.nextInt();
            attempt+=1;


            if(num<numtbg){
                System.out.println("too low,try again buddy");

            } else if (num>numtbg) {
                System.out.println("too high , try again buddy");

            }

            else if(num==numtbg){
                System.out.printf("good ,  it took u %s attempts",attempt);
            }

        }
        while (!(num == numtbg));


            pain.close();
        }
    }

