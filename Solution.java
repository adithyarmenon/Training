class ListNode {
    int data;
    ListNode next;
    ListNode(int key) { 
        data = key; 
    }
}

class Solution {
    public ListNode reverseKGroup(ListNode head, int k) {
        ListNode curr = head, count = head;
        int i = 0;
        
        while (count != null && i < k) {
            count = count.next;
            i++;
        }
        
        if (i == k) {
            count = reverseKGroup(count, k);
            while (i-- > 0) {
                ListNode temp = curr.next;
                curr.next = count;
                count = curr;
                curr = temp;
            }
            head = count;
        }
        return head;
    }
    
    public static void main(String[] args) {
        Solution sol = new Solution();
        
        // Test case: 1->2->3->4->5->6 with k=2
        ListNode head = new ListNode(1);
        head.next = new ListNode(2);
        head.next.next = new ListNode(3);
        head.next.next.next = new ListNode(4);
        head.next.next.next.next = new ListNode(5);
        head.next.next.next.next.next = new ListNode(6);
        
        System.out.print("Original: ");
        printList(head);
        
        ListNode result = sol.reverseKGroup(head, 2);
        System.out.print("Reversed (k=2): ");
        printList(result);
    }
    
    static void printList(ListNode head) {
        while (head != null) {
            System.out.print(head.data);
            if (head.next != null) System.out.print("->");
            head = head.next;
        }
        System.out.println();
    }
}