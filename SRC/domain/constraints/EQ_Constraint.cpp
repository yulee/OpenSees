/* ****************************************************************** **
**    OpenSees - Open System for Earthquake Engineering Simulation    **
**          Pacific Earthquake Engineering Research Center            **
**                                                                    **
**                                                                    **
** (C) Copyright 1999, The Regents of the University of California    **
** All Rights Reserved.                                               **
**                                                                    **
** Commercial use of this program without express permission of the   **
** University of California, Berkeley, is strictly prohibited.  See   **
** file 'COPYRIGHT'  in main directory for information on usage and   **
** redistribution,  and for a DISCLAIMER OF ALL WARRANTIES.           **
**                                                                    **
** Developed by:                                                      **
**   Frank McKenna (fmckenna@ce.berkeley.edu)                         **
**   Gregory L. Fenves (fenves@ce.berkeley.edu)                       **
**   Filip C. Filippou (filippou@ce.berkeley.edu)                     **
**                                                                    **
** ****************************************************************** */
                                                                        
// $Revision: 1.5 $
// $Date: 2010-04-23 22:50:19 $
// $Source: /usr/local/cvs/OpenSees/SRC/domain/constraints/EQ_Constraint.cpp,v $
                                                                        
                                                                        
// Written: fmk 
// Created: 11/96
// Revision: A
//
// Purpose: This file contains the implementation of class EQ_Constraint.
//
// The class EQ_Constraint interface:
//

#include <EQ_Constraint.h>

#include <stdlib.h>
#include <Matrix.h>
#include <ID.h>
#include <Channel.h>
#include <FEM_ObjectBroker.h>
#include <elementAPI.h>
#include <Domain.h>
#include <Node.h>

static int numEQs = 0;
static int nextTag = 0;

int OPS_EquationConstraint()
{
    Domain* theDomain = OPS_GetDomain();
    if (theDomain == 0) {
	    opserr<<"WARNING: domain is not defined\n";
	    return -1;
    }

    int numRemainingArgs = OPS_GetNumRemainingInputArgs();
    if(numRemainingArgs < 6 || numRemainingArgs % 3) {
	    opserr<<"WARNING: invalid # of args: equationConstraint cNodeTag cdof ccoef rNodeTag1 rdof1 rcoef1 rNodeTag2 rdof2 rcoef2 ...\n";
	    return -1;
    }

    int numData = 1;
    int cNode, cDOF;
    if(OPS_GetIntInput(&numData, &cNode)) {
        opserr<<"WARNING invalid cNodeTag inputs\n";
        return -1;
    }
    if(OPS_GetIntInput(&numData, &cDOF)) {
        opserr<<"WARNING invalid cDOF inputs\n";
        return -1;
    }
    cDOF--;
    double cc = 0.0;
    if (OPS_GetDouble(&numData, &cc) || cc == 0.0) {
        opserr<<"WARNING invalid ccoef inputs\n";
        return -1;
    }

    int rdf = numRemainingArgs / 3 - 1;
    ID rNode(rdf);
    ID rDOF(rdf);
    
     // constraint matrix
    Matrix Ccr(1,rdf);

    for(int i = 0; i < rdf; i++) {
        int rNodei, rDOFi;
        if(OPS_GetIntInput(&numData, &rNodei)) {
            opserr<<"WARNING invalid rNodeTag inputs\n";
            return -1;
        }
        if(OPS_GetIntInput(&numData, &rDOFi)) {
            opserr<<"WARNING invalid rDOF inputs\n";
            return -1;
        }
        double rci;
        if (OPS_GetDouble(&numData, &rci)) {
            opserr<<"WARNING invalid rcoef inputs\n";
            return -1;
        }
        rNode(i) = rNodei;
        rDOF(i) = rDOFi - 1;
        Ccr(1,i) = -rci / cc;
    }

    opserr << "yhyh:\n";
    opserr << "rdf" << rdf << "\n";
    opserr << "numRemainingArgs" << numRemainingArgs << "\n";
    opserr << "yhyh:" << Ccr;

    EQ_Constraint* theEQ = new EQ_Constraint(cNode,cDOF,Ccr,rNode,rDOF);
    if(theEQ == 0) {
	    opserr<<"WARNING: failed to create EQ_Constraint\n";
	    return -1;
    }
    if(theDomain->addEQ_Constraint(theEQ) == false) {
	    opserr<<"WARNING: failed to add EQ_Constraint to domain\n";
	    delete theEQ;
	    return -1;
    }
    return 0;
}

// constructor for FEM_ObjectBroker
EQ_Constraint::EQ_Constraint(int clasTag )		
:DomainComponent(nextTag++, clasTag),
 nodeRetained(0),nodeConstrained(0),constraint(0),constrDOF(0),retainDOF(0), initialized(false),
 dbTag1(0), dbTag2(0)
{
  numEQs++;
}

// constructor for Subclass
EQ_Constraint::EQ_Constraint(int nodeConstr, int constrainedDOF, 
			     ID &nodeRetain, ID &retainedDOF, int clasTag)
:DomainComponent(nextTag++, clasTag),
 nodeRetained(0), nodeConstrained(nodeConstr), 
 constraint(0), constrDOF(constrainedDOF), retainDOF(0), initialized(false), dbTag1(0), dbTag2(0)
{
    numEQs++;
  
    nodeRetained = new ID(nodeRetain);
    retainDOF = new ID(retainedDOF);    
    if (nodeRetained == 0 || nodeRetain.Size() != nodeRetained->Size() ||
            retainDOF == 0 || retainedDOF.Size() != retainDOF->Size()) { 
        opserr << "EQ_Constraint::EQ_Constraint - ran out of memory 1\n";
        exit(-1);
    }    

    // resize initial state
    Uc0 = 0.0;
    Ur0.resize(retainDOF->Size());
    Ur0.Zero();
}


// general constructor for ModelBuilder
EQ_Constraint::EQ_Constraint(int nodeConstr, int constrainedDOF, Matrix &constr,
                                ID &nodeRetain, ID &retainedDOF)
:DomainComponent(nextTag++, CNSTRNT_TAG_EQ_Constraint), 
nodeRetained(0), nodeConstrained(nodeConstr), 
constraint(0), constrDOF(constrainedDOF), retainDOF(0), initialized(false), dbTag1(0), dbTag2(0)
{
    numEQs++;    
    nodeRetained = new ID(nodeRetain);
    retainDOF = new ID(retainedDOF);    
    if (nodeRetained == 0 || nodeRetain.Size() != nodeRetained->Size() ||
            retainDOF == 0 || retainedDOF.Size() != retainDOF->Size()) { 
        opserr << "EQ_Constraint::EQ_Constraint - ran out of memory 1\n";
        exit(-1);
    }    
    
    constraint = new Matrix(constr);
    if (constraint == 0 || constr.noCols() != constr.noCols()) { 
        opserr << "MP_Constraint::MP_Constraint - ran out of memory 2\n";
        exit(-1);
    }        
    
    // resize initial state
    Uc0 = 0.0;
    Ur0.resize(retainDOF->Size());
    Ur0.Zero();
}



EQ_Constraint::~EQ_Constraint()
{
    // invoke the destructor on the matrix and the two ID objects
    if (constraint != 0)
	delete constraint;
    if (nodeRetained != 0)
	delete nodeRetained;
    if (retainDOF != 0)
	delete retainDOF;    
    
    numEQs--;
    if (numEQs == 0)
        nextTag = 0;
}

void EQ_Constraint::setDomain(Domain* theDomain)
{
    // store initial state
    if (theDomain) {
        if (!initialized) {
            Node* theConstrainedNode = theDomain->getNode(nodeConstrained);
            if (theConstrainedNode == 0) {
                opserr << "FATAL EQ_Constraint::setDomain() - Constrained or Retained";
                opserr << " Node does not exist in Domain\n";
                opserr << nodeConstrained << endln;
                exit(-1);
            }
            const Vector& Uc = theConstrainedNode->getTrialDisp();
            int cdof = getConstrainedDOFs();
            if (cdof < 0 || cdof >= Uc.Size()) {
                opserr << "EQ_Constraint::setDomain FATAL Error: Constrained DOF " << cdof << " out of bounds [0-" << Uc.Size() - 1 << "]\n";
                exit(-1);
            }
            Uc0 = Uc(cdof);
            initialized = true;
            const ID& idr = getRetainedDOFs();
            for (int i = 0; i < nodeRetained->Size(); ++i) {
                Node* theRetainedNode = theDomain->getNode((*nodeRetained)(i));
                if (theRetainedNode == 0) {
                    opserr << "FATAL EQ_Constraint::setDomain() - Constrained or Retained";
                    opserr << " Node does not exist in Domain\n";
                    opserr << nodeRetained << endln;
                    exit(-1);
                }
                const Vector& Ur = theRetainedNode->getTrialDisp();
                int rdof = idr(i);
                if (rdof < 0 || rdof >= Ur.Size()) {
                    opserr << "EQ_Constraint::setDomain FATAL Error: Retained DOF " << rdof << " out of bounds [0-" << Ur.Size() - 1 << "]\n";
                    exit(-1);
                }
                Ur0(i) = Ur(rdof);
            }
        }
    }

    // call base class implementation
    DomainComponent::setDomain(theDomain);
}

const ID &
EQ_Constraint::getNodeRetained(void) const
{
    if (nodeRetained == 0) {
        opserr << "EQ_Constraint::getNodeRetained - no ID was set, ";
        opserr << "was recvSelf() ever called? or subclass incorrect?\n";	
        exit(-1);
    }

    // return the ID corresponding to retained nodes
    return *nodeRetained;    
}

int
EQ_Constraint::getNodeConstrained(void) const
{
    // return id of constrained node    
    return nodeConstrained;
}


int
EQ_Constraint::getConstrainedDOFs(void) const
{
    // return the ID corresponding to constrained DOF of Ccr
    return constrDOF;    
}


const ID &
EQ_Constraint::getRetainedDOFs(void) const
{
    if (retainDOF == 0) {
        opserr << "EQ_Constraint::getRetainedDOFs - no ID was set\n ";
        opserr << "was recvSelf() ever called? or subclass incorrect?\n";		
        exit(-1);
    }

    // return the ID corresponding to retained DOF of Ccr
    return *retainDOF;    
}

int 
EQ_Constraint::applyConstraint(double timeStamp)
{
    // does nothing EQ_Constraint objects are time invariant
    return 0;
}

bool
EQ_Constraint::isTimeVarying(void) const
{
    return false;
}


const Matrix &
EQ_Constraint::getConstraint(void)
{
    if (constraint == 0) {
        opserr << "EQ_Constraint::getConstraint - no Matrix was set\n";
        exit(-1);
    }    

    // return the constraint matrix Ccr
    return *constraint;    
}

double EQ_Constraint::getConstrainedDOFsInitialDisplacement(void) const
{
    return Uc0;
}

const Vector& EQ_Constraint::getRetainedDOFsInitialDisplacement(void) const
{
    return Ur0;
}

int 
EQ_Constraint::sendSelf(int cTag, Channel &theChannel)
{
/*
    static ID data(11);
    int dataTag = this->getDbTag();

    data(0) = this->getTag(); 
    data(1) = nodeRetained;
    data(2) = nodeConstrained;
    if (constraint == 0) data(3) = 0; else data(3) = constraint->noRows();
    if (constraint == 0) data(4) = 0; else data(4) = constraint->noCols();    
    if (constrDOF == 0) data(5) = 0; else data(5) = constrDOF->Size();    
    if (retainDOF == 0) data(6) = 0; else data(6) = retainDOF->Size();        
    
    // need two database tags for ID objects
    if (constrDOF != 0 && dbTag1 == 0) 
      dbTag1 = theChannel.getDbTag();
    if (retainDOF != 0 && dbTag2 == 0) 
      dbTag2 = theChannel.getDbTag();

    data(7) = dbTag1;
    data(8) = dbTag2;
    data(9) = nextTag;
    data(10) = static_cast<int>(initialized);

    int result = theChannel.sendID(dataTag, cTag, data);
    if (result < 0) {
	opserr << "WARNING EQ_Constraint::sendSelf - error sending ID data\n";
	return result;  
    }    
    
    if (constraint != 0 && constraint->noRows() != 0) {
	int result = theChannel.sendMatrix(dataTag, cTag, *constraint);
	if (result < 0) {
	    opserr << "WARNING EQ_Constraint::sendSelf ";
	    opserr << "- error sending Matrix data\n"; 
	    return result;  
	}
    }

    if (constrDOF != 0 && constrDOF->Size() != 0) {
	int result = theChannel.sendID(dbTag1, cTag, *constrDOF);
	if (result < 0) {
	    opserr << "WARNING EQ_Constraint::sendSelf ";
	    opserr << "- error sending constrained data\n"; 
	    return result;  
	}
    }

    if (retainDOF != 0 && retainDOF->Size() != 0) {
	int result = theChannel.sendID(dbTag2, cTag, *retainDOF);
	if (result < 0) {
	    opserr << "WARNING EQ_Constraint::sendSelf ";
	    opserr << "- error sending retained data\n"; 
	    return result;  
	}
    }
    
    // send initial displacement vectors.
    // we need 2 database tags because they have the same size,
    // but we can reuse the tags used for ID objects, since they go into different files
    if (Uc0.Size() > 0) {
        int result = theChannel.sendVector(dbTag1, cTag, Uc0);
        if (result < 0) {
            opserr << "WARNING EQ_Constraint::sendSelf ";
            opserr << "- error sending constrained initial displacement\n";
            return result;
        }
    }
    if (Ur0.Size() > 0) {
        int result = theChannel.sendVector(dbTag2, cTag, Ur0);
        if (result < 0) {
            opserr << "WARNING EQ_Constraint::sendSelf ";
            opserr << "- error sending retained initial displacement\n";
            return result;
        }
    }
*/
    return 0;
}


int 
EQ_Constraint::recvSelf(int cTag, Channel &theChannel, 
			FEM_ObjectBroker &theBroker)
{
/*
    int dataTag = this->getDbTag();
    static ID data(11);
    int result = theChannel.recvID(dataTag, cTag, data);
    if (result < 0) {
	opserr << "WARNING EQ_Constraint::recvSelf - error receiving ID data\n";
	return result;  
    }    

    this->setTag(data(0));
    nodeRetained = data(1);
    nodeConstrained = data(2);
    int numRows = data(3); 
    int numCols = data(4);
    dbTag1 = data(7);
    dbTag2 = data(8);
    nextTag = data(9);
    initialized = static_cast<bool>(data(10));

    if (numRows != 0 && numCols != 0) {
	constraint = new Matrix(numRows,numCols);
	
	int result = theChannel.recvMatrix(dataTag, cTag, *constraint);
	if (result < 0) {
	    opserr << "WARNING EQ_Constraint::recvSelf ";
	    opserr << "- error receiving Matrix data\n"; 
	    return result;  
	}
    }    
    int size = data(5);
    if (size != 0) {
	constrDOF = new ID(size);
	int result = theChannel.recvID(dbTag1, cTag, *constrDOF);
	if (result < 0) {
	    opserr << "WARNING EQ_Constraint::recvSelf ";
	    opserr << "- error receiving constrained data\n"; 
	    return result;  
	}	
    }
    
    size = data(6);
    if (size != 0) {
	retainDOF = new ID(size);
	int result = theChannel.recvID(dbTag2, cTag, *retainDOF);
	if (result < 0) {
	    opserr << "WARNING EQ_Constraint::recvSelf ";
	    opserr << "- error receiving retained data\n"; 
	    return result;  
	}	
    }    
    
    // recv initial displacement vectors.
    // we need 2 database tags because they have the same size,
    // but we can reuse the tags used for ID objects, since they go into different files
    if (constrDOF && constrDOF->Size() > 0)
        Uc0.resize(constrDOF->Size());
    else
        Uc0 = Vector();
    if (retainDOF && retainDOF->Size() > 0)
        Ur0.resize(retainDOF->Size());
    else
        Ur0 = Vector();
    if (Uc0.Size() > 0) {
        int result = theChannel.recvVector(dbTag1, cTag, Uc0);
        if (result < 0) {
            opserr << "WARNING EQ_Constraint::recvSelf ";
            opserr << "- error receiving constrained initial displacement\n";
            return result;
        }
    }
    if (Ur0.Size() > 0) {
        int result = theChannel.recvVector(dbTag2, cTag, Ur0);
        if (result < 0) {
            opserr << "WARNING EQ_Constraint::recvSelf ";
            opserr << "- error receiving retained initial displacement\n";
            return result;
        }
    }
*/
    return 0;
}



void
EQ_Constraint::Print(OPS_Stream &s, int flag)
{     
/*
    s << "EQ_Constraint: " << this->getTag() << "\n";
    s << "\tNode Constrained: " << nodeConstrained;
    s << " node Retained: " << nodeRetained << "\n";
    if (constrDOF != 0 && retainDOF != 0) {
      s << " constrained dof: ";
      for (int i=0; i<(*constrDOF).Size(); i++)
	s << (*constrDOF)(i)+1 << " ";
      s << endln;
	s << " retained dof: ";        
      for (int i=0; i<(*retainDOF).Size(); i++)
	s << (*retainDOF)(i)+1 << " ";
      s << endln;
      if (constraint != 0)
	s << " constraint matrix: " << *constraint << "\n";
    }
*/
}


