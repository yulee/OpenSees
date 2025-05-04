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
// $Source: /usr/local/cvs/OpenSees/SRC/domain/constraints/EQ_Constraint.h,v $
                                                                        
                                                                        
#ifndef EQ_Constraint_h
#define EQ_Constraint_h

// Written: Yuli Huang 
// Created: 11/96
// Revision: A
//
// Purpose: This file contains the class definition for EQ_Constraint.
// EQ_Constraint is a class which stores the information for a multi
// point constraint. A multipoint constraint relates certain dof at 
// a constrained node to be related to certain dof at a retained node: 
//                      {Uc} = [Ccr] {Ur}
//
// The EQ_Constraint class assumes time invariant constraints, i.e. the
// constraint matrix does not change over time. All the methods are declared
// as pure virtual, which will allow subclasses for time varying constraints.
//
// What: "@(#) EQ_Constraint, revA"

#include <DomainComponent.h>

class Matrix;
class ID;

class EQ_Constraint : public DomainComponent
{
  public:
    // constructors        
    EQ_Constraint(int classTag ); // Arash

    EQ_Constraint(int nodeConstr, 
      int constrainedDOF,
      ID &nodeRetain, 
      ID &retainedDOF,
      int classTag);    

    EQ_Constraint(int nodeConstr, 
		  int constrainedDOF,
		  Matrix &constrnt,
      ID &nodeRetain,
    	ID &retainedDOF);

    // destructor    
    virtual ~EQ_Constraint();

    // domain component
    void setDomain(Domain* theDomain);

    // method to get information about the constraint
    virtual const ID &getNodeRetained(void) const;
    virtual int getNodeConstrained(void) const;    
    virtual int getConstrainedDOFs(void) const;        
    virtual const ID &getRetainedDOFs(void) const;            
    virtual int applyConstraint(double pseudoTime);
    virtual bool isTimeVarying(void) const;
    virtual const Matrix &getConstraint(void);    
    virtual const Vector &getConstrainedDOFsInitialDisplacement(void) const;
    virtual const Vector &getRetainedDOFsInitialDisplacement(void) const;

    // methods for output
    virtual int sendSelf(int commitTag, Channel &theChannel);
    virtual int recvSelf(int commitTag, Channel &theChannel, 
       FEM_ObjectBroker &theBroker);
    
    virtual void Print(OPS_Stream &s, int flag =0);

  protected:
    
  private:
    ID *nodeRetained;        // to identify the retained node
    int nodeConstrained;     // to identify  the constrained node
    Matrix *constraint;      // pointer to the constraint matrix
    int constrDOF;           // ID of constrained DOF at constrained node
    ID *retainDOF;           // ID of related DOF at retained node
    double Uc0;              // initial displacement at constrained DOFs (same size as constrDOF)
    Vector Ur0;              // initial displacement at retained node  (same size as retainDOF)
    bool initialized;        // a flag to avoid recomputing the intial values in setDomain if already initialized
    int dbTag1, dbTag2;      // need a dbTag for the two ID's
};

#endif

