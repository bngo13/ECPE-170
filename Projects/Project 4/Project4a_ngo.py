# Parse Argument
import argparse
parser = argparse.ArgumentParser(description='Input: input file, Memory;')
parser.add_argument("inF")
parser.add_argument("memF")
args = parser.parse_args()

class ProgramCounter:
	def __init__(self):
		self.count = 0
		
		self.sll = 0
		self.pcsrc = 0

	def get_count(self):
		return self.count

	def next_count(self):
		if self.pcsrc == 0:
			self.count = self.count + 4
		else:
			self.count = self.count + 4 + self.sll
		
		# Reset
		self.sll = 0
		self.pcsrc = 0

	def set_sll(self, sll):
		self.sll = sll
	
	def set_pcsrc(self, pcsrc):
		self.pcsrc = pcsrc

class InstructionMemory:
	def __init__(self):
		# Read Argument
		instruction_file = open(args.inF, "r")
		
		instruct_data = instruction_file.read()
		
		# Split lines by new line
		self.instruct_list = instruct_data.split("\n")
		
		if len(self.instruct_list) > 100:
			self.instruct_list = []
		
		instruction_file.close()

	def get_instruct(self, progcount):
		return self.instruct_list[progcount // 4]

class Control:
	def __init__(self):
		self.control_dict = {
			# Order: RegDst, ALUSrc, MemtoReg, RegWrite, MemRead, MemWrite, branch, ALUOp1 ALUOp2, Zero bit
			
			# R Type
			"000000": [1,0,0,1,0,0,0,1,0,0],
			
			# Other Types
			"001000": [0,1,0,1,0,0,0,0,0,0], # addi
			"000100": [0,0,0,0,0,0,1,0,1,1], # beq
			"000101": [0,0,0,0,0,0,1,1,1,0], # bne
			"100011": [0,1,1,1,1,0,0,0,0,0], # lw
			"101011": [0,1,0,0,0,1,0,0,0,0], # sw
		}
		self.control_list = [0,0,0,0,0,0,0,0,0,0]

	def set_control(self, name):
		self.control_list = self.control_dict.get(name)

	def get_control(self):
		return self.control_list

class Registers:
	def __init__(self):
		self.registers = {
			"00000": 0,
			"00001": 0,
			"00010": 0,
			"00011": 0,
			"00100": 0,
			"00101": 0,
			"00110": 0,
			"00111": 0
		}
		
		self.regwrite = 0
		
		self.readreg1 = ""
		self.readreg2 = ""
		self.writereg = ""
	
	def set_regwrite(self, regwrite):
		self.regwrite = regwrite
	
	def set_readreg1(self, rr1):
		self.readreg1 = rr1
	
	def set_readreg2(self, rr2):
		self.readreg2 = rr2
	
	def set_writereg(self, wr):
		self.writereg = wr
	
	def get_readreg1(self):
		return self.registers.get(self.readreg1)
	
	def get_readreg2(self):
		return self.registers.get(self.readreg2)
	
	def write_data(self, data):
		if self.registers.get(self.writereg) != None and self.regwrite == 1:
			self.registers.update({self.writereg: data})

class ALU:
	def __init__(self):
		# Default R
		self.alucontrol = []
		self.functfields = {
			"100000": "add",
			"100010": "sub",
		}
		
		# Funct
		self.funct = "000000"
		
		# Inputs
		self.input1 = 0
		self.input2 = 0
	
	def set_alucontrol(self, alucontrol):
		self.alucontrol = alucontrol
	
	def set_funct(self, funct):
		self.funct = funct

	def execute(self):
		if self.alucontrol == [0, 0]:
			return self.input1 + self.input2
		elif self.alucontrol == [1, 0]:
			funct = self.functfields.get(self.funct)
			if funct == "add":
				
				return self.input1 + self.input2
			elif funct == "sub":
				return self.input1 - self.input2
			else:
				print("NOT FOUND")
		elif self.alucontrol == [0, 1]:
			if self.input1 - self.input2 == 0:
				counter.set_pcsrc(1)
			return self.input1 + self.input2
		elif self.alucontrol == [1, 1]:
			if self.input1 - self.input2 != 0:
				counter.set_pcsrc(1)
			return self.input1 + self.input2

class DataMemory:
	def __init__(self):
		self.current_addr = 0
		self.addresses = {}
		self.memwrite = 0
		self.memread = 0
		
		self.load_memory_file()
	
	def load_memory_file(self):
		# Load "memory" file into actual memory
		memoryF = open(args.memF, 'r')
		memory = memoryF.read()
		memory = memory.split("\n")
		i = 1
		
		# Update our memory of data
		for address in memory:
			try:
				isBool = False
				
				# Check for negatives
				if "-" in address:
					isBool = True
					address = address.replace("-","")
				
				data = int(address)
				
				# Put the negative back
				if isBool:
					data = data * -1
				
			except:
				data = 0
			
			self.addresses.update({i:data})
			i += 1
		
		memoryF.close()
	
	def set_memwrite(self, memwrite):
		self.memwrite = memwrite
	
	def set_memread(self, memread):
		self.memread = memread
	
	def set_address(self, address):
		self.current_addr = address
	
	def read_data(self):
		if self.memread == 1:
			potentialData = self.addresses.get(self.current_addr)
			if potentialData == None:
				return 0
			return potentialData
	
	def write_data(self, data):
		# Update our copy of addresses
		if self.memwrite == 1:
			
			print(data)
			self.addresses.update({self.current_addr: data})
			self.addresses = dict(sorted(self.addresses.items()))
			
			# Write to memory file
			output = ""
			
			memFile = open(args.memF, 'w')
			
			lineNum = 1
			
			for k, v in self.addresses.items():
				while lineNum < k:
					output += "0\n"
					lineNum += 1
				output += str(v) + "\n"
				lineNum += 1
			
			output = output[:-1]
			
			memFile.write(output)
			
		#memFile = open(args.memF, 'w')
		
		

# Data Parts
counter = ProgramCounter()
instructMem = InstructionMemory()
control = Control()
registers = Registers()
alu = ALU()
datamem = DataMemory()

def main():
	registerPrint = ""
	controlPrint = ""
	
	# Get control signals
	while True:
		count = counter.get_count()
		try:
			instruction = instructMem.get_instruct(count)
		except:
			counter.count = 0
			break
		if instruction == "":
			counter.count = 0
			break
		# Parse Instruction
		opcode = instruction[0:6]
		
		# Set Control
		
		control.set_control(opcode)
		control_list = control.get_control()
		controlPrint += prettyPrintControl(control_list) + "\n"
		counter.next_count()
	
	# Start actually processing
	while True:
		# Next Line
		count = counter.get_count()
		
		registerPrint += prettyPrintRegisters() + "\n"
		try:
			instruction = instructMem.get_instruct(count)
		except:
			break
		if instruction == "":
			break
		# Parse Instruction
		opcode = instruction[0:6]
		rs = instruction[6:11]
		rt = instruction[11:16]
		rd = instruction[16:21]
		immediate = instruction[16:]
		
		# Set Control
		
		control.set_control(opcode)
		control_list = control.get_control()
		
		# Get Registers
		
		registers.set_readreg1(rs)
		rsData = registers.get_readreg1()
		registers.set_readreg2(rt)
		rtData = registers.get_readreg2()
		registers.set_regwrite(control_list[3])
		
		if control_list[0] == 0:
			registers.set_writereg(rt)
		else:
			registers.set_writereg(rd)
		
		# Sign Extend immediate
		immediate = twos_comp(int(immediate,2), len(immediate))
		
		# Update Program Counter
		counter.set_sll(immediate << 2)
		
		# Set ALU Inputs
		alu.input1 = rsData
		if control_list[1] == 0:
			alu.input2 = rtData
		else:
			alu.input2 = immediate
		
		# Set ALU Control
		alu.set_funct(instruction[-6:])
		alu.set_alucontrol([control_list[7], control_list[8]])
		
		aluResult = alu.execute()
		
		# Process Data Memory Portion
		datamem.set_memwrite(control_list[5])
		datamem.set_memread(control_list[4])
		
		datamem.set_address(aluResult)
		memoryData = datamem.read_data()
		datamem.write_data(rtData)
		
		# Choose MemtoReg
		registerWriteData = 0
		
		if control_list[2] == 1:
			registerWriteData = memoryData
		else:
			registerWriteData = aluResult
		
		registers.write_data(registerWriteData)
		
		# Go to the next count
		counter.next_count()
		reset_devices()

	if (counter.get_count() // 4) > len(instructMem.instruct_list):
		controlPrint = "!!! Segmentation Fault !!!\r\n"
		registerPrint = "!!! Segmentation Fault !!!\r\n"
	
	# Save to respective files
	saveControl(controlPrint)
	saveRegisters(registerPrint)

def twos_comp(val, bits):
	if (val & (1 << (bits - 1))) != 0:
		val = val - (1 << bits)
	return val

def reset_devices():
	control.__init__()
	alu.__init__()

def prettyPrintControl(control_list):
	output = ""
	for c in control_list:
		output += str(c)
	return output

def prettyPrintRegisters():
	output = ""
	output += f"{65536 + counter.get_count()}|"
	for register in registers.registers.values():
		output += f"{register}|"
	output = output[:-1]
	
	return output

def saveControl(control):
	controlFile = open("control.txt", 'w')
	controlFile.write(control)
	controlFile.close()

def saveRegisters(register):
	controlFile = open("registers.txt", 'w')
	controlFile.write(register)
	controlFile.close()

if __name__ == "__main__":
	main()