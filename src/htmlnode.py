class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None or len(self.props) == 0:
            return ""
        html = ""
        sorted_props = dict(sorted(self.props.items(), key=lambda item: item[0]))
        for k, v in sorted_props.items():
            if k == "style" and type(v) == dict:
                sorted_css = sorted(v.items(), key=lambda item: item[0])
                inline_style = ""
                for style in sorted_css:
                    inline_style += f"{style[0]}:{style[1]}; "
                html += f'style="{inline_style[:-1]}" '
            else:
                html += f'{k}="{v}" '
        return " " + html[:-1]

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Value required")
        if self.tag is None:
            return f"{self.value}"

        single_tags = ["img", "input"]

        if self.tag in single_tags:
            return f"<{self.tag}{self.props_to_html()}>"

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag required")

        if self.children is None:
            raise ValueError("Children required")

        children_html = ""
        for child in self.children:
            children_html += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
