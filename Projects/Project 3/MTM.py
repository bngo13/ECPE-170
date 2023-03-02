'''
MIPS REFERENCE
	Add	: 000000	rs	rt	rd	sa	100000 	| sa = 00000
	Sub	: 000000	rs	rt	rd	sa	100010	| sa = 00000
	SLL	: 000000	rs	rt	rd	sa	000000		| ra = 00000
	SRL	: 000000	rs	rt	rd	sa	000010		| ra = 00000
	SLT	: 000000	rs	rt	rd	sa	101010	| sa = 00000

	Addi: 001000	rs	rt	imm
	BEQ	: 000100	rs	rt	offset
	BNE	: 000101	rs	rt	offset
	LW	: 100011	rs	rt	offset
	SW	: 101011	rs	rt	offset
'''
import argparse

# Set constants
R_LIST = [
	"add", 
	"sub", 
	"sll", 
	"srl", 
	"slt"
]
R_BINARY = [
	["000000", "", "", "", "", "100000"], 
	["000000", "", "", "", "", "100010"], 
	["000000", "", "", "", "", "000000"], 
	["000000", "", "", "", "", "000010"], 
	["000000", "", "", "", "", "101010"]
]

I_LIST = [
	"addi", 
	"beq", 
	"bne", 
	"lw", 
	"sw"
]
I_BINARY = [ # Append at beginning of binary string
	["001000", "", "", ""], 
	["000100", "", "", ""], 
	["000101", "", "", ""], 
	["100011", "", "", ""], 
	["101011", "", "", ""]
]

REGISTER_LISTS = [
	"zero",
	"at",
	"v0", "v1",
	"a0", "a1", "a2", "a3",
	"t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7",
	"s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7",
	"t8", "t9",
	"k0", "k1",
	"gp",
	"sp",
	"s8",
	"ra"
]


# Start function defs
def parse_instruction(input_string):
	failedParse = ["!!! invalid input !!!"]
	'''
		OpCode
	'''
	instructionType = "rtype"
	instructionToReg = input_string.split(" ", 1)
	
	# Check if input is RList or not
	if not (instructionToReg[0] in R_LIST or instructionToReg[0] in I_LIST):
		return failedParse
	
	template = parse_instruc_to_binary(instructionToReg[0])
	if instructionToReg[0] in I_LIST:
		instructionType = "itype"
	
	'''
		Registers
	'''
	instructionToReg[1] = instructionToReg[1].replace(" ", "")
	regList = instructionToReg[1].split(",")
	
	# Check for regList being the right size
	if len(regList) != 3 and len(regList) != 2:
		return failedParse
		
	if instructionType == "rtype":
		if not parse_rtype(instructionToReg[0], template, regList):
			return failedParse
	else:
		if not parse_itype(instructionToReg[0], template, regList):
			return failedParse
	return template
	
def parse_instruc_to_binary(stringin):
	# stringin = instruction input
	if stringin in R_LIST:
		index = R_LIST.index(stringin)
		return R_BINARY[index]
	index = I_LIST.index(stringin)
	return I_BINARY[index]

def parse_rtype(opcode, template, registers):
	# opcode: string of opcode
	# template: list type
	# registers: list of registers 
	
	# init variables for conversions
	rs = ""
	rt = ""
	rd = ""
	sa = ""
	if opcode == "add" or opcode == "sub" or opcode == "slt":
		# Preset registers for conversions
		rs = registers[1]
		rt = registers[2]
		rd = registers[0]
		sa = "0"
	elif opcode == "sll" or opcode == "srl":
		# Preset registers for conversions
		rs = "$zero"
		rt = registers[1]
		rd = registers[0]
		sa = registers[2]
	else:
		return False
	
	i = 1
	# Cover rs, rt, rd
	for register in [rs, rt, rd]:
		number = 0
		
		# Test if in register
		if not ("$" in register):
			
			print(register)
			return False
		# Remove dollar sign
		register = register.replace("$", "")
		
		# Convert to register number 
		if register in REGISTER_LISTS:
			number = REGISTER_LISTS.index(register)
		elif register.isnumeric():
			number = int(register)
		else:
			return False
		
		if number > 31:
			return False
		# Conver to binary
		template[i] = int_to_binary(5, number)
		
		i += 1
	
	''' Cover for SA '''
	# If not number then not good
	if not sa.isnumeric():
		return False
	
	# Convert and test for number boundaries
	number = int(sa)
	if number >= 32 or number < 0:
		return False
	
	# Convert int to binary
	binary = int_to_binary(5, number)
	
	# Test for length of string
	if len(binary) != 5:
		return False
	template[4] = binary
	
	return True
	
def parse_itype(opcode, template, registers):
	# opcode: string of opcode
	# template: list type
	# registers: list of registers 
	
	# init variables for conversions
	rt = ""
	rs = ""
	offset = 0
	
	# Test for opcodes
	if opcode == "addi":
		rt = registers[0]
		rs = registers[1]
		offset = registers[2]
		if offset.replace("-", "").isnumeric():
			number = int(offset)
		else:
			return False
		offset = number
	elif opcode == "beq" or opcode == "bne":
		rt = registers[1]
		rs = registers[0]
		offset = registers[2]
		number = 0
		
		# Divide offset by 4
		if offset.replace("-", "").isnumeric():
			number = int(offset)
		else:
			return False
		offset = number // 4
	elif opcode == "lw" or opcode == "sw":
		rt = registers[0]
		
		# Pull offset from second section
		rsoffset = registers[1].split("(")
		offset = rsoffset[0]
		rs = rsoffset[1].replace(")", "")
		number = 0
		
		# Convert offset to number
		if offset.replace("-", "").isnumeric():
			number = int(offset)
		else:
			return False
		offset = number
	else:
		return False
	
	i = 1
	for register in [rs, rt]:
		number = 0
		
		# Make sure $ is in the register name
		if not ("$" in register):
			return False
		
		# Remove $
		register = register.replace("$", "")
		
		# Get register number
		if register in REGISTER_LISTS:
			number = REGISTER_LISTS.index(register)
		elif register.isnumeric():
			number = int(register)
		else:
			return False

		# Check boundaries
		if number > 31 or number < 0:
			return False
		
		# Convert to binary
		template[i] = int_to_binary(5, number)
		
		i += 1
	
	''' Parse offset '''
	# Convert to binary
	binary = int_to_binary(16, offset)
	
	# Make sure length is correct
	if len(binary) != 16:
		return False
	template[3] = binary
	
	return True

def int_to_binary(size, number):
	# If negative, bit shift to negative numbers
	if number < 0:
		number = (1 << size) + number
	
	# Create formatting
	formatting = '{:0%ib}' % size
	return formatting.format(number)

def parse_args():
	parser = argparse.ArgumentParser(description='Input: input file\nOutput: output file')
	parser.add_argument("--input", dest='inputF', required=True)
	#parser.add_argument("--output", dest='outputF', required=True)
	return parser.parse_args()

def read_file(filename):
	openf = open(filename, 'r')
	lines = openf.readlines()
	return lines

def save_to_file(filename, output):
	openf = open(filename, 'w')
	openf.write(output)
	openf.close()

def main():
	args = parse_args()
	args.outputF = "out_code.txt"
	infile = args.inputF
	
	lines = read_file(infile)
	output = ""
	for line in lines:
		# Default line as valid
		valid = True
		line = line.replace("\n", "")
			
		commentIndex = line.find('#');
		if commentIndex != -1:
			line = line.split('#', 1)[0]
		
		line = line.strip()
		
		if len(line)  == 0:
			output += "\n"
			continue
		
		for section in parse_instruction(line):
			output += section
			if section == "!!! invalid input !!!":
				valid = False
				break
		if valid == False:
			break
		output += "\n"
	
	save_to_file(args.outputF, output)

if __name__ == "__main__":
	main()
