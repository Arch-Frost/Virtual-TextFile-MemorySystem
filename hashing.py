import math

def hash_data(plain_text):

    # print(plain_text)
    sum = 0
    for i in range(0, len(plain_text), 2):
        if i < len(plain_text)-1:
            sum += ord(plain_text[i]) * ord(plain_text[i+1])
        else:
            sum += ord(plain_text[i])

    hash_string = ""

    for i in range(1, 257):
        if i % 6 == 1:
            char_1 = math.sin(sum + i)
            char_2 = math.cos(sum + i)
            char_3 = 2 * char_1 ** 2
            char_4 = 3 * char_2 ** 3
            char_5 = char_1 * char_2 + char_3
            char_6 = char_1 - 5 * char_2
        elif i % 6 == 2:
            char_1 = math.sin(sum - i)
            char_2 = math.cos(sum - i)
            char_3 = 2 * char_1 ** 3
            char_4 = 3 * char_2 ** 2
            char_5 = char_2 * char_1 + char_3
            char_6 = char_1 + 4 * char_2
        elif i % 6 == 3:
            char_1 = math.sin(sum + 2 * i)
            char_2 = math.cos(sum + 2 * i)
            char_3 = 2 * char_1 ** 2 - 3
            char_4 = 3 * char_2 ** 2 + 4
            char_5 = char_1 * char_2 + char_4
            char_6 = char_1 - 2 * char_2
        elif i % 6 == 4:
            char_1 = math.sin(sum - 2 * i)
            char_2 = math.cos(sum - 2 * i)
            char_3 = 2 * char_1 ** 3 + 5
            char_4 = 3 * char_2 ** 3 - 6
            char_5 = char_1 * char_2 - char_3
            char_6 = char_2 - 3 * char_1
        elif i % 6 == 5:
            char_1 = math.sin(sum + i**2)
            char_2 = math.cos(sum + i**2)
            char_3 = 2 * char_1 ** 2 + 1
            char_4 = 3 * char_2 ** 2 - 1
            char_5 = char_1 * char_2 + char_3
            char_6 = char_2 - char_1
        else:
            char_1 = math.sin(sum - i**2)
            char_2 = math.cos(sum - i**2)
            char_3 = 2 * char_1 ** 3 + 1
            char_4 = 3 * char_2 ** 2 - 2
            char_5 = char_1 * char_2 - char_3
            char_6 = char_2 + 2 * char_1

        mega_char = ((abs(int(char_1 * 100)) * abs(int(char_2 * 100)))/100 + (abs(int(char_3 * 100)) *
                    abs(int(char_4 * 100)))/100 + (abs(int(char_5 * 100)) * abs(int(char_6 * 100)))/100
    )
            # Concatenate each transformation to the hash string
        hash_string += chr(abs(int(mega_char))%128)

    return hash_string


if __name__=="__main__":
    plain_text = "In today’s fast-paced digital world, technology is constantly evolving, shaping every aspect of our lives. From the way we communicate to the way we work and even how we entertain ourselves, technological advancements have made a significant impact. Artificial intelligence, for instance, has revolutionized industries ranging from healthcare to finance, providing innovative solutions to long-standing challenges. The internet of things (IoT) is connecting everyday objects, making them smarter and more efficient. As we move further into the 21st century, it's clear that the future of technology holds even more transformative potential, and it will be exciting to see how it continues to shape our world in the years to come."
    print(hash_data(plain_text))