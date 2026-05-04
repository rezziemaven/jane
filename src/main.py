from textnode import TextNode, TextType


def main():
    tn = TextNode("Hello World!", TextType.TEXT, "https://google.com")
    print(tn)


main()
