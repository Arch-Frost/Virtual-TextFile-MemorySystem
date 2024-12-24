import math

prevents = [0, 7, 8, 9, 10, 11, 12, 13, 14, 15, 27, 32, 95, 127, 128, 129, 130, 131, 132, 133, 134,
          135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152,
          153, 154, 155, 156, 157, 158, 159, 160, 173]


def hash_data(plain_text):

    # print(plain_text)
    sum = 0
    for i in range(0, len(plain_text), 2):
        if i < len(plain_text)-1:
            sum += ord(plain_text[i]) * ord(plain_text[i+1])
        else:
            sum += ord(plain_text[i])

    hash_string = ""
    n = len(plain_text)

    for i in range(1, 64):
        if i % 6 == 1:
            char_1 = math.sin(sum + i + ord(plain_text[i%n]))
            char_2 = math.cos(sum + i + ord(plain_text[i%n]))
            char_3 = 2 * char_1 ** 2
            char_4 = 3 * char_2 ** 3
            char_5 = char_1 * char_2 + char_3
            char_6 = char_1 - 5 * char_2
        elif i % 6 == 2:
            char_1 = math.sin(sum - i - ord(plain_text[i%n]))
            char_2 = math.cos(sum - i + ord(plain_text[i%n]))
            char_3 = 2 * char_1 ** 3
            char_4 = 3 * char_2 ** 2
            char_5 = char_2 * char_1 + char_3
            char_6 = char_1 + 4 * char_2
        elif i % 6 == 3:
            char_1 = math.sin(sum + 2 * i + ord(plain_text[i%n]))
            char_2 = math.cos(sum + 2 * i - ord(plain_text[i%n]))
            char_3 = 2 * char_1 ** 2 - 3
            char_4 = 3 * char_2 ** 2 + 4
            char_5 = char_1 * char_2 + char_4
            char_6 = char_1 - 2 * char_2
        elif i % 6 == 4:
            char_1 = math.sin(sum - 2 * i - ord(plain_text[i%n]))
            char_2 = math.cos(sum - 2 * i + ord(plain_text[i%n]))
            char_3 = 2 * char_1 ** 3 + 5
            char_4 = 3 * char_2 ** 3 - 6
            char_5 = char_1 * char_2 - char_3
            char_6 = char_2 - 3 * char_1
        elif i % 6 == 5:
            char_1 = math.sin(sum + i**2 * ord(plain_text[i%n]))
            char_2 = math.cos(sum + i**2 * ord(plain_text[i%n]))
            char_3 = 2 * char_1 ** 2 + 1
            char_4 = 3 * char_2 ** 2 - 1
            char_5 = char_1 * char_2 + char_3
            char_6 = char_2 - char_1
        else:
            char_1 = math.sin(sum - i**2 + 3*ord(plain_text[i%n]))
            char_2 = math.cos(sum - i**2 - math.sin(ord(plain_text[i%n])))
            char_3 = 2 * char_1 ** 3 + 1
            char_4 = 3 * char_2 ** 2 - 2
            char_5 = char_1 * char_2 - char_3
            char_6 = char_2 + 2 * char_1

        mega_char = ((abs(int(char_1 * 100)) * abs(int(char_2 * 100))) + (abs(int(char_3 * 100)) *
                    abs(int(char_4 * 100))) + (abs(int(char_5 * 100)) * abs(int(char_6 * 100))))
        
        bounded_mega_char = mega_char%256
        if bounded_mega_char in prevents:
            bounded_mega_char += 66

        hash_string += chr(bounded_mega_char)

    return hash_string


if __name__=="__main__":
    # plain_text = "In today’s fast-paced digital world, technology is constantly evolving, shaping every aspect of our lives. From the way we communicate to the way we work and even how we entertain ourselves, technological advancements have made a significant impact. Artificial intelligence, for instance, has revolutionized industries ranging from healthcare to finance, providing innovative solutions to long-standing challenges. The internet of things (IoT) is connecting everyday objects, making them smarter and more efficient. As we move further into the 21st century, it's clear that the future of technology holds even more transformative potential, and it will be exciting to see how it continues to shape our world in the years to come."
    # print(hash_data(plain_text))
    plain_text_1 = "arha"
    plain_text_2 = "haar"
    hash_1 = hash_data(plain_text_1)
    hash_2 = hash_data(plain_text_2)
    print(plain_text_1)
    print(hash_1)
    print(plain_text_2)
    print(hash_2)
    hash_3 = hash_data("a")
    print("a")
    print(hash_3)
    hash_3 = hash_data(".")
    print(".")
    print(hash_3)