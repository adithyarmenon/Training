import java.util.Scanner;
public class LychrelProcess {
    public static long[] findPalindrome(long n, int k) {
        for (int i = 0; i < k; i++) {
            long reversed = reverse(n);
            n += reversed;
            if (isPalindrome(n)) return new long[]{i + 1, n};
        }
        return new long[]{-1, -1};
    }
    private static long reverse(long num) {
        long rev = 0;
        while (num > 0) {
            rev = rev * 10 + num % 10;
            num /= 10;
        }
        return rev;
    }
    private static boolean isPalindrome(long num) {
        return num == reverse(num);
    } 
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.print("Enter value of n: ");
        long n = input.nextLong();
        System.out.println("Enter value of k: ");
        int k = input.nextInt();        
        long[] result = findPalindrome(n,k);
        System.out.println("[" + result[0] + ", " + result[1] + "]");
        input.close();
    }
}