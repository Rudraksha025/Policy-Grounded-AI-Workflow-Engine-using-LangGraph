# class ListNode():
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

# def reverse(head):
#     curr = head
#     prev = None

#     while curr:
#         next_node = curr.next
#         curr.next = prev 
#         prev = curr
#         curr = next_node
#     return prev

# head = ListNode(1)
# head.next = ListNode(2)
# head.next.next = ListNode(3)
# head.next.next.next = ListNode(4)

# new_head = reverse(head)

# while new_head:
#     print(new_head.val, end="->")
#     new_head = new_head.next
# print("None")


from shared.utils import get_policy_retriever

retriever = get_policy_retriever()
docs = retriever.invoke("credit score below 600")

print("\n".join(d.page_content for d in docs))
