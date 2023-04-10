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

def parse_args():
	parser = argparse.ArgumentParser(prog='PyCaching', description='Caching Emulation')
	
	parser.add_argument('--type', choices=['d', 's'], dest='cacheType', required=True)
	parser.add_argument('--cache_size', type=int, dest='cacheSize', required=True)
	parser.add_argument('--block_size', type=int, dest='blockSize', required=True)
	parser.add_argument('--memfile', dest='memFile', required=True)
	args =  parser.parse_args()
	return args

DC = DirectCache()

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
	#print(args.cacheType)
	
	block_size = args.blockSize
	cache_size = args.cacheSize
	block_bits = int(math.log2(args.blockSize)) 
	cache_bits = int(math.log2(args.cacheSize))
	
	DC.__init__(args.cacheSize, args.blockSize)
	
	#memoryAddress = ["50", "50", "D0", "D0"]
	
	# Load file into list
	memFile = open(args.memFile, 'r')
	memFileContents = memFile.read().strip()
	memoryAddress = memFileContents.split("\n")
	#print(memoryAddress)
	
	
	# Direct Caching
	hitOrMiss = ""
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
			
		#print(json.dumps(DC.cache_list, sort_keys=True, indent=4))
	print(hitOrMiss)

def hexToBin(hexString):
	n = int(hexString, 16)
	hexBin = bin(n)[2:].zfill(32)
	return hexBin

if __name__ == "__main__":
	main()