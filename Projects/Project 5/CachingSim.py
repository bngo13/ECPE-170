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
	def __init__(self, cache_size=0, block_size=0, way=0):
		# Cache List line: [Valid, Set ID, cache_dict: {dict of blocks in cache way}]
		self.cache_list = {}
		for i in range(0, way):
			cache_dict = {}
			for j in range(0, cache_size // way):
			# cache_line: [Tag Bit, blocks: {dict of blocks}]
				blockDict = {}
				for k in range(0, block_size):
					blockDict.update({
						k: [0,0,0,0]
					})
				cache_dict.update({
					j: [
						0,
						blockDict
					]
				})
			self.cache_list.update({
				i: [
					0,
					0,
					cache_dict
				]
			})
	def find_address(self, way_bit, tag_bit):
		# Find set 
		found_set = self.cache_list.get(way_bit)
		if found_set == None:
			return False
		
		# Check Valid Bit
		if found_set[0] == 0:
			return False
		
		# Check for tag bit
		for address in found_set.values():
			if address == tag_bit:
				return True
		return False
	
	def write_address(self, way_bit, tag_bit):
		# Find set
		found_set = self.cache_list.get(way_bit)
		found_set[0] = 0
		
		# Create new entry
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
	# Byte Offset
	byteOffset = memBin[-2:]
	memBin = memBin[:-2]
	#print("Byte Offset: ", byteOffset)
	
	# Word Offset
	
	wordOffset = memBin[block_size:]
	memBin = memBin[:block_size]
	#print("Word Offset: ", wordOffset)
	
	# Index Bits
	indexBits = memBin[cache_size:]
	memBin = memBin[:cache_size]
	#print("Index Size: ", indexBits)
	
	# Rest of bits
	tagBits = memBin
	#print("Tag: ", memBin)
	
	return (tagBits, indexBits, wordOffset, byteOffset)

def main():
	args = parse_args()
	isDirectCaching = True
	if args.cacheType == 's':
		isDirectCaching = False
	
	block_size = args.blockSize
	cache_size = args.cacheSize
	block_bits = int(math.log2(block_size // 4))
	cache_bits = int(math.log2(cache_size))
	print(f"Cache Lines: {cache_bits}\nBits per block: {block_bits}")
	
	# Initialize Caching Types
	DC.__init__(cache_size, block_size)
	
	# Load file into list
	memFile = open(args.memFile, 'r')
	memFileContents = memFile.read().strip()
	memoryAddress = memFileContents.split("\n")
	#print(memoryAddress)
	
	# Calculating Hit Rates
	total = 0
	hit = 0
	hitOrMiss = ""
	
	# Direct Caching
	if isDirectCaching:
		if args.setAssociativeWays != None:
			print("Additional Parameter: set_ways was set for direct cache mapping")
			return
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
			
			# Check for alignment
			if int(memBin, 2) % 4 != 0:
				hitOrMiss += f"{address}|{dcResult[0]}|{dcResult[1]}|Unaligned\n"
				continue
			#print(json.dumps(DC.cache_list, sort_keys=True, indent=4))
			
			if DC.inCache(indexBits, wordOffset, tagBits) == False:
				hitOrMiss += f"{address}|{dcResult[0]}|{dcResult[1]}|Miss\n"
				DC.writeCache(indexBits, block_size, tagBits)
			else:
				hitOrMiss += f"{address}|{dcResult[0]}|{dcResult[1]}|Hit\n"
				hit += 1
				
			#print(json.dumps(DC.cache_list, sort_keys=True, indent=4))
			total += 1
	else:
		# Init SAC
		if args.setAssociativeWays == None:
			print("set_ways argument required")
			return
		way_size = args.setAssociativeWays
		way_bits = int(math.log2(way_size))
		SAC.__init__(cache_size, block_size, way_size)
		
		# Check for alignment? TODO
		
		# Start
		#print(SAC.cache_list)
		
		SAC.find_address()
		
		print(json.dumps(SAC.cache_list, sort_keys=True, indent=4))
		hit = 1
		total = 1
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