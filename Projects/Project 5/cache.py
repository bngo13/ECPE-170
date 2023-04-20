import math
import argparse

import json

class DirectCache:
	def __init__(self, cache_size=0, block_size=0):
		# cache_line: [Valid, Tag Bit, blocks: {dict of blocks}]
		self.cache_list = {}
		for i in range(0, cache_size):
			blockDict = {}
			for j in range(0, block_size):
				blockDict.update({
						j: [0,0,0,0]
					})
			self.cache_list.update({
					i: [
						0,
						0,
						blockDict
					]
				})
	def inCache(self, cache_line, block_number, tag_bit):
		# Find cache line
		cacheLine = self.cache_list.get(cache_line)
		if cacheLine == None:
			return False
		
		# Check Valid Bit
		if cacheLine[0] == 0:
			return False
		
		# Check Tag Bit
		if cacheLine[1] != tag_bit:
			return False
			
		# if cacheLine[2].get(block_number) == None:
		# 	return False
		
		return True
	
	def writeCache(self, cache_line, block_size, tag_bit):
		blockDict = {}
		for j in range(0, block_size):
			blockDict.update({
					j: [0,0,0,0]
				})
		
		self.cache_list.update({
				cache_line: [
								1,
								tag_bit,
								blockDict
							]
			})

class SetAssociativeCache:
	def __init__(self, set_count=0, block_count=0, n_way=1):
		self.DC_list = []
		# Create N-Way DC 
		for i in range(0, n_way):
			DC = {}
			for j in range(0, set_count):
				DC_block = {}
				for k in range(0, block_count):
					DC_block.update({k: [0,0,0,0]})
				DC.update({j: [
					0, # Tag Bit
					0, # Valid
					0, # Count
					DC_block
				]})
			self.DC_list.append(DC)
			
	def find_address(self, tag_bit, set_number):
		for dc in self.DC_list:
			if dc.get(set_number) != None and dc.get(set_number)[0] == tag_bit and dc.get(set_number)[1] != 0:
				return True
		return False

	def write_address(self, tag_bit, set_number):
		# Increment Counter
		for dc in self.DC_list:
			for block in dc.values():
				block[2] += 1
		
		smallerValue = 0
		smallerIndex = self.DC_list[0].get(set_number)
		for dc in self.DC_list:
			if dc.get(set_number)[2] > smallerValue:
				smallerValue = dc.get(set_number)[2]
				smallerIndex = dc.get(set_number)
		
		smallerIndex[0] = tag_bit
		smallerIndex[1] = 1
		smallerIndex[2] = 0
				
def parse_args():
	parser = argparse.ArgumentParser(prog='PyCaching', description='Caching Emulation')
	
	parser.add_argument('--type', choices=['d', 's'], dest='cacheType', required=True)
	parser.add_argument('--cache_size', type=int, dest='cacheSize', required=True)
	parser.add_argument('--block_size', type=int, dest='blockSize', required=True)
	parser.add_argument('--set_ways', type=int, dest='setAssociativeWays', required=False)
	parser.add_argument('--memfile', dest='memFile', required=True)
	args =  parser.parse_args()
	return args

DC = DirectCache()
SAC = SetAssociativeCache()

def parseDC(memBin, block_size, cache_size):
	# print("---")
	# print(memBin)
	# print(cache_size)
	# print(block_size)
	# print("---")
	# Byte Offset
	byteOffset = memBin[-2:]
	memBin = memBin[:-2]
	# print("Byte Offset: ", byteOffset)
	
	# Word Offset
	if block_size == 0:
		wordOffset = '0'
		memBin = memBin[:-1]
	else:
		wordOffset = memBin[block_size:]
		memBin = memBin[:block_size]
	# print("Word Offset: ", wordOffset)
	
	# Index Bits
	if cache_size == 0:
		indexBits = '0'
		memBin = memBin[:-1]
	else:
		indexBits = memBin[cache_size:]
		memBin = memBin[:cache_size]
	# print("Index Size: ", indexBits)
	
	# Rest of bits
	if memBin == '':
		tagBits = '0'
	else:
		tagBits = memBin
	
	# print("Tag: ", memBin)
	
	return (tagBits, indexBits, wordOffset, byteOffset)

def parseSAC(memBin, set_size, block_size):
	# print("---")
	# print(memBin)
	# print(set_size)
	# print(block_size)
	# print("---")
	
	#print(memBin)
	# Byte Offset
	byteOffset = memBin[-2:]
	memBin = memBin[:-2]
	
	# Block Offset
	if block_size == 0:
		blockOffset = "0"
	else:
		blockOffset = memBin[block_size:]
		memBin = memBin[:block_size]
	
	# Set Offset
	if set_size == 0:
		setOffset = "0"
	else:
		setOffset = memBin[set_size:]
		memBin = memBin[:set_size]
	
	# Tag Bits
	tagBits = memBin
	return (tagBits, setOffset, blockOffset, byteOffset)

def main():
	args = parse_args()
	isDirectCaching = True
	if args.cacheType == 's':
		isDirectCaching = False
	
	block_size = args.blockSize
	cache_size = args.cacheSize
	
	if block_size // 4 < 1:
		block_bits = 0
	else:
		block_bits = math.ceil(math.log2(block_size // 4))
	cache_bits = math.ceil(math.log2(cache_size))
	# print(f"Cache Lines: {cache_bits}\nBits per block: {block_bits}")
	
	# Initialize Caching Types
	DC.__init__(cache_size, block_size)
	
	# Load file into list
	memFile = open(args.memFile, 'r')
	memFileContents = memFile.read().strip()
	memoryAddress = memFileContents.split("\n")
	
	# # Convert mem address to hex if int
	# for i in range(0, len(memoryAddress)):
	# 	memoryAddress[i] = hex(int(memoryAddress[i]))
	
	# Calculating Hit Rates
	total = 0
	hit = 0
	hitOrMiss = ""
	
	# Direct Caching
	if isDirectCaching:
		for address in memoryAddress:
			
			memBin = hexToBin(address)
			#print(int(memBin, 2))
			#continue
			#print(memBin)
			dcResult = parseDC(memBin, block_bits * -1, cache_bits * -1)
			tagBits = int(dcResult[0], 2)
			indexBits = int(dcResult[1], 2)
			wordOffset = int(dcResult[2], 2)
			byteOffset = int(dcResult[3], 2)
			
			output = ""
			
			# Check for alignment
			#print(json.dumps(DC.cache_list, sort_keys=True, indent=4))
			
			if DC.inCache(indexBits, wordOffset, tagBits) == False:
				output = "Miss"
				DC.writeCache(indexBits, block_size, tagBits)
			else:
				output = "Hit"
				hit += 1
			
			if int(memBin, 2) % 4 != 0:
				output = "Misaligned"
			
			hitOrMiss += f"{address}|{dcResult[0]}|{dcResult[1]}|{output}\n"
			
			#print(json.dumps(DC.cache_list, sort_keys=True, indent=4))
			total += 1
	else:
		# Init SAC
		if args.setAssociativeWays == None:
			print("set_ways argument required")
			return
		way_size = args.setAssociativeWays
		way_bits = math.ceil(math.log2(way_size))
		SAC.__init__(cache_size, block_size, way_size)
		
		# Start
		for address in memoryAddress:
			
			memBin = hexToBin(address)
			splitSAC = parseSAC(memBin, cache_bits * -1, block_bits * -1)
			#print(splitSAC)
			tagBits = int(splitSAC[0], 2)
			setNumber = int(splitSAC[1], 2)
			wordIndex = int(splitSAC[2], 2)
			byteoffset = int(splitSAC[3], 2)
			
			output = ""
			
			print(SAC.find_address(tagBits, setNumber))
			print(splitSAC)
			if not SAC.find_address(tagBits, setNumber):
				output = "Miss"
				SAC.write_address(tagBits, setNumber)
			else:
				output = "Hit"
				hit += 1
			total += 1
			
			if int(memBin, 2) % 4 != 0:
				output = "Misaligned"
			
			hitOrMiss += f"{address}|{splitSAC[0]}|{splitSAC[1]}|{output}\n"
			
		if total == 0:
			total = 1
		
		#print(json.dumps(SAC.DC_list, sort_keys=True, indent=4))
		
	write_result(f"{hitOrMiss}\nHit Rate: {(hit / total) * 100}")

def write_result(output):
	fOpen = open('cache.txt', 'w')
	fOpen.write(output)
	fOpen.close()

def hexToBin(hexString):
	n = int(hexString, 16)
	hexBin = bin(n)[2:].zfill(32)
	return hexBin

if __name__ == "__main__":
	main()