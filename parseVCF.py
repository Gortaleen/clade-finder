# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 16:07:43 2020

@author: hunte
"""

import vcf
import sys
import tabix
from Common import CommonMethods

def getPositionSNP(position, allele, tb):
    try:
        positionResults = tb.querys(position + ":1-1")
        for snp in positionResults:
            if snp[4] == allele:
                return snp[3], "+"
            else:
                return snp[3], "-"
        return None, None
    except:
        return None, None
        
if len(sys.argv) > 2:
    vcfFile = sys.argv[1]
    tbPositionSNPsFile = sys.argv[2]
    tbCladeSNPFile = sys.argv[3]
    tbSNPcladeFile = sys.argv[4]
    
def isMale(vcfFile):
    return True

def parseBases(basesString):
    basesSplits = basesString.split("/")
    if len(basesSplits) == 2:
        call1 = basesSplits[0]
        call2 = basesSplits[1]
        if call1 == call2:
            return call1
        return None
    else:
        if len(basesSplits) == 1:
            return basesSplits[0]
    return None

def parseVCF(vcfFile, tbPositionSNPsFile):
    tbPositionSNPs = tabix.open(tbPositionSNPsFile)
    positives = []
    negatives = []
    if isMale(vcfFile):    
        vcf_reader = vcf.Reader(filename=vcfFile)
        record = next(vcf_reader)
        
        
        while record:
            if record.CHROM == "chrY":
                position = str(record.POS)
                basesString = record.samples[0].gt_bases
                if basesString:
                    allele = parseBases(basesString)
                    if allele:
                        (snp, call) = getPositionSNP(position, allele, tbPositionSNPs)
                        if snp:
                            if call == "+":
                                positives.append(snp)
                            else:
                                negatives.append(snp)
                            
                            #print(posSNP)
                try:
                    record = next(vcf_reader)
                except:
                    record = None
    
    return positives, negatives
def getSNPsBelowClade(clade, tb):
    children = CommonMethods.getChildrenTabix(clade, tb)
    thesesnps = CommonMethods.getCladeSNPs(clade, tb)
    snps = []
    for snp in thesesnps:
        snps.append(snp)
    for child in children:
        childSNPs = getSNPsBelowClade(child, tb)
        for childSNP in childSNPs:
            snps.append(childSNP)
    return snps

def filterSNPsTopTwoPredictions(jsonObj, positives, negatives, tbCladeSNPFile, tbSNPcladeFile):
    #tbCladeSNPs = tabix.open(tbCladeSNPFile)
    
    return jsonObj

import time
start_time = time.time()

#(positives, negatives) = parseVCF(vcfFile, tbPositionSNPsFile)
parsed_time = time.time()
print ('parsing vcf ' + str(parsed_time - start_time) + ' seconds')
#jsonObj = CommonMethods.getJSON("score", positives, negatives, tbCladeSNPFile, tbSNPcladeFile, None)
found_time = time.time()
print ('found clade in ' + str(found_time - parsed_time) + ' seconds')
#(positives, negatives) = filterSNPsTopTwoPredictions(jsonObj, positives, negatives, tbCladeSNPFile, tbSNPcladeFile)
tb = tabix.open(tbCladeSNPFile)
print (", ".join(getSNPsBelowClade("J-Z1043", tabix)))
print (", ".join(getSNPsBelowClade("J-PH1080", tabix)))