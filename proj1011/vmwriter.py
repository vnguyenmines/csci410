
class VMWriter:
    def __init__(self, output_path):
        self.output_file = open(output_path, "w+")
        self.output_lines = []

    def write_push(self, segment, index: int):
        self.output_lines.append("push {} {}".format(segment, index))

    def write_pop(self, segment, index: int):
        self.output_lines.append("pop {} {}".format(segment, index))

    def write_arithmetic(self):
        pass

    def write_label(self, label):
        self.output_lines.append("label {}".format(label))

    def write_goto(self, label):
        self.output_lines.append("goto {}".format(label))

    def write_if(self, label):
        self.output_lines.append("")
        self.output_lines.append("if-goto {}".format(label))

    def write_call(self, class_name, function_name, arg_c):
        self.output_lines.append("call {}.{} {}".format(class_name, function_name, arg_c))

    def write_function(self):
        pass

    def write_return(self):
        self.output_lines.append("return")

    def write(self):
        self.output_file.writelines(self.output_lines)