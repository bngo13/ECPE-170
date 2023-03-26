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
		instruction_file = open("alpha.bin", "r")
		instruct_data = instruction_file.read()
		
		self.instruct_list = instruct_data.split("\n")
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
			"001000": [0,1,0,1,0,0,0,0,0,0]
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
		
		self.regwrite = False
		
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
		if self.registers.get(self.writereg) != None:
			self.registers.update({self.writereg: data})

class ALU:
	def __init__(self):
		# Default R
		self.alucontrol = []
		self.functfields = {
			"100000": "add",
			"100010": "sub",
			"100100": "and",
			"100101": "or",
			"101010": "slt"
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
			elif funct == "and":
				print("PERFORM AND")
			elif funct == "or":
				print("PERFORM OR")
			elif funct == "slt":
				print("PERFORM SLT")
			else:
				print("NOT FOUND")
		elif self.alucontrol == [0, 1]:
			print("DO BEQ")
		else:
			print("DO BNE")

class DataMemory:
	# Unused for now
	def __init__(self):
		self.current_addr = 0
		self.addresses = {}
		self.memwrite = False
		self.memread = False
	
	def set_memwrite(self, memwrite):
		self.memwrite = memwrite
	
	def set_memread(self, memread):
		self.memread = memread
	
	def set_address(self, address):
		self.current_addr = address
	
	def read_data(self):
		if self.memread == True:
			return self.addresses.get(self.current_addr)
	
	def write_data(self, data):
		if self.memwrite == True:
			self.addresses.update({self.current_addr: data})

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
	while True :
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
		controlPrint += prettyPrintControl(control_list) + "\n"
		
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
		immediate = int(immediate, 2)
		
		# Update Program Counter
		counter.set_sll(immediate << 2)
		
		alu.input1 = rsData
		if control_list[1] == 0:
			alu.input2 = rtData
		else:
			alu.input2 = immediate
		
		alu.set_funct(instruction[-6:])
		alu.set_alucontrol([control_list[7], control_list[8]])
		
		aluResult = alu.execute()
		
		datamem.set_address(aluResult)
		memoryData = datamem.read_data()
		datamem.write_data(rtData)
		
		registerWriteData = 0
		
		if control_list[2] == 1:
			registerWriteData = memoryData
		else:
			registerWriteData = aluResult
		
		registers.write_data(registerWriteData)
		counter.next_count()
	
	saveControl(controlPrint)
	saveRegisters(registerPrint)

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