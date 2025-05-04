import os

class VMWriter:
    def __init__(self, output_path):
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        self.output_file = open(output_path, "w")
        self.output_lines = []

    def write_push(self, segment, index: int):
        self.output_lines.append("push {} {}".format(segment, index))

    def write_pop(self, segment, index: int):
        self.output_lines.append("pop {} {}".format(segment, index))

    def write_arithmetic(self, op):
        self.output_lines.append(op)

    def write_int(self, val):
        self.write_push("constant", val)
    
    def write_string(self, string_to_write):
        self.write_int(len(string_to_write))
        self.write_call("String", "new", 1)
        for current_char in string_to_write:
            self.write_int(ord(current_char))
            self.write_call("String", "appendChar", 2)

    def write_label(self, label):
        self.output_lines.append("label {}".format(label))

    def write_goto(self, label):
        self.output_lines.append("goto {}".format(label))

    def write_if(self, label):
        self.output_lines.append("if-goto {}".format(label))

    def write_call(self, class_name, function_name, arg_c):
        self.output_lines.append("call {}.{} {}".format(class_name, function_name, arg_c))

    def write_function(self, class_name, func_name, local_var_count):
        self.output_lines.append("function {}.{} {}".format(class_name, func_name, local_var_count))

    def write_return(self):
        self.output_lines.append("return")

    def write_vm_file(self):
        for line in self.output_lines:
            if "label" not in line and "function" not in line:
                self.output_file.write("\t" + line + "\n")
            else:
                self.output_file.write(line + "\n")