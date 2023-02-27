import os
import sys
import math
import adsk.core, adsk.fusion, traceback
######################################################################
AN=1900
##########################################
def LireLesDebits(ANNEE):
#    DEBIT=[1900,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]        
#    DEBIT=[1900,500,500,500,500,500,500,500,500,500,500,500,500,500,500,500]        
#    DEBIT=[1900,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000]        
#    DEBIT=[1900,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500]        
    DEBIT=[1900,2000,2000,2000,2000,2000,2000,2000,2000,2000,2000,2000,2000,2000,2000,2000]        
    print(DEBIT)
    print(DEBIT[1:5])
    print(ANNEE)
    # Lire le fichier qui contient les débits / mois, 1 ligne /an
    cFichier="D:\CNC\projet_AL\CruesLoire1964_2022_an-DJF-DJF.txt"
    f = open(cFichier, 'r', encoding="utf-8")
    for k in range(0,58):
        LIGNE=f.readline()
#        print(LIGNE)    
#       string[start:end:step] une partie de la chaine de caractère
#        print (">"+LIGNE[1:5]+"<","   ",">"+str(ANNEE)+"<")
        if LIGNE[1:5]==str(ANNEE):
            print (LIGNE[1:5]," = ",str(ANNEE),"EGALITE")
            #on a trouvé la ligne contenant les débits
            #lecture de la ligne contenant des valeurs séparées par des ;
            CAR=" "
            j=0
            LIGNE=str(LIGNE)
            MOT=""
            for i in range(1,len(LIGNE)):
#                print(str(i)+"-")
                CAR=LIGNE[i:i+1]
                if (CAR==";"):
#                    print(MOT)    
                    DEBIT[j]=MOT
                    MOT=""
                    j=j+1
                else:
                    MOT=MOT+CAR
    f.close()
    return DEBIT
########################################################################""    
def run(context):
    ui = None
    try: 
        app = adsk.core.Application.get()
        ui = app.userInterface

        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = app.activeProduct

        # Get the root component of the active design.
        rootComp = design.rootComponent

        # Create a new sketch on the xy plane.
        sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)

        # Create an object collection for the points.
        points = adsk.core.ObjectCollection.create()
        
   
        #lire les crues de l'année voulue
  
        debits=LireLesDebits(AN)
        print(debits)

        PHI=-0      #math.pi/6
        RAYON_0=1               #rayon 0 m3/s = 1 cm
        ECHELLE=0.01    #mm/m3.S
        for i in range (2,15):
            # garder en mémoire le premier et le dernier point
            if PHI==0:
                x=(ECHELLE*float(debits[i])+RAYON_0)*math.cos(PHI)
                y=0.155
                x1=x
                y1=y
            elif i==14:
                x=(ECHELLE*float(debits[i])+RAYON_0)*math.cos(PHI)
                y=-0.155
                x2=x
                y2=y
            else:    
                # Define the points the spline with fit through.
                x=(ECHELLE*float(debits[i])+RAYON_0)*math.cos(PHI)
                y=(ECHELLE*float(debits[i])+RAYON_0)*math.sin(PHI)
                # Define the points the spline with fit through.
            points.add(adsk.core.Point3D.create(x,y, 0))
            PHI=PHI+math.pi/6
        
        # Create the spline.
        spline = sketch.sketchCurves.sketchFittedSplines.add(points)

        # Get spline fit points
        fitPoints = spline.fitPoints
        
        # Get the second fit point
        fitPoint = fitPoints.item(1)
################################################################################################## 
#         
        # If there is no the relative tangent handle, activate the tangent handle
#        line = spline.getTangentHandle(fitPoint)
#        if line is None:
#             line = spline.activateTangentHandle(fitPoint)
                
        # Get the tangent handle           
#        gottenLine = spline.getTangentHandle(fitPoint)
        
        # Delete the tangent handle
#        gottenLine.deleteMe()

        # Activate the curvature handle
        # If the curvature handle activated. the relative tangentHandle is activated automatically
#        activatedArc= spline.activateCurvatureHandle(fitPoint)
        
        # Get curvature handle and tangent handle
#        gottenArc= spline.getCurvatureHandle(fitPoint)
#        gottenLine = spline.getTangentHandle(fitPoint)
        
        # Delete curvature handle
#        gottenArc.deleteMe();

########################################################## C E R C L E S
        #tracer un arc (trou de 10mm dia non fermé (+-1.5mm))
   #     startPoint = adsk.core.Point2D.create(0.05, 0.15)
   #     point= = adsk.core.Point2D.create(-0.05, 0)
   #     endPoint= adsk.core.Point2D.create(0.05, -0.15)
   #     returnValue = adsk.core.Arc2D.createByThreePoints(startPoint, point, endPoint)

        #calcul point à h mm audessus de l'axe xx sur le cercle de rayon 5mm
        angle=math.asin(1.55/5)
        x3=0.5*math.cos(angle)
        arcs = sketch.sketchCurves.sketchArcs
        arcs.addByCenterStartSweep(adsk.core.Point3D.create(0,0,0),adsk.core.Point3D.create(x3,0.155,0),2*math.pi-2*angle)

        # Draw some circles. rayon 0.5cm centré et à 20 mm rayon 0.4mm
        circles = sketch.sketchCurves.sketchCircles
#        circle1 = circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), 0.5)
        circle2 = circles.addByCenterRadius(adsk.core.Point3D.create(0, 1, 0), 0.4)
#        circle3 = circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), 1)

######################### ligne entre les points extrêmes#######################
#         # Create sketch line
        sketchLines = sketch.sketchCurves.sketchLines

#        PHI=-0      #math.pi/6
#        i=2
#        x=(ECHELLE*float(debits[i])+RAYON_0)*math.cos(PHI)
#        y=(ECHELLE*float(debits[i])+RAYON_0)*math.sin(PHI)
#        startPoint = adsk.core.Point3D.create(x, y, 0)
#        i=14
#        x=(ECHELLE*float(debits[i])+RAYON_0)*math.cos(PHI)
#        y=(ECHELLE*float(debits[i])+RAYON_0)*math.sin(PHI)
#        endPoint = adsk.core.Point3D.create(x, y, 0)
#        sketchLineOne = sketchLines.addByTwoPoints(startPoint, endPoint)


        startPoint = adsk.core.Point3D.create(x3,0.155, 0)
        endPoint = adsk.core.Point3D.create(x1, 0.155, 0)
        sketchLineOne = sketchLines.addByTwoPoints(startPoint, endPoint)

        startPoint = adsk.core.Point3D.create(x3,-0.155, 0)
        endPoint = adsk.core.Point3D.create(x2, -0.155, 0)
        sketchLineOne = sketchLines.addByTwoPoints(startPoint, endPoint)
#############################################################################################""

        # Create a new sketch on the XY construction plane.
        sk = rootComp.sketches.add(rootComp.xYConstructionPlane)

        # Get the SketchTexts collection object.
        texts = sk.sketchTexts
        
        # Add multi-line text.
        AN_=str(AN)[2:5]
        input = texts.createInput2(AN_,3)
        input.setAsMultiLine(adsk.core.Point3D.create(0.5, 3.5, 0),
                             adsk.core.Point3D.create(4, 0.2, 0),
                             adsk.core.HorizontalAlignments.LeftHorizontalAlignment,
                             adsk.core.VerticalAlignments.TopVerticalAlignment, 0)
        texts.add(input)

        # Draw an arc to use to create text along a curve.
#        arc = sk.sketchCurves.sketchArcs.addByThreePoints(adsk.core.Point3D.create(-10, 0, 0),
#                                                          adsk.core.Point3D.create(-5, 3, 0),
#                                                          adsk.core.Point3D.create(0, 0, 0))

        # Create text along the arc.
#        input = texts.createInput2('Text Along a Curve', 0.75)
#        input.setAsAlongPath(arc, False, adsk.core.HorizontalAlignments.CenterHorizontalAlignment, 0)
#        input.isHorizontalFlip = True
#        input.isVerticalFlip = True
#        input.fontName = 'Comic Sans MS'
#        texts.add(input)        
         
        # Get the profile of the first sketch
#        prof = sketch.profiles.item(0)
           
            # Create an extrusion input
#        extrudes1 = subComp1.features.extrudeFeatures
#        extInput1 = extrudes1.createInput(prof1, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
#        extrudes = rootComp.features.extrudeFeatures
#        extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        
        # Define that the extent is a distance extent of 0.5 cm
#        distance = adsk.core.ValueInput.createByReal(-0.5)
        # Set the distance extent
#        extInput.setDistanceExtent(False, distance)
        # Set the extrude type to be solid
#        extInput.isSolid = True
        
        # Create the extrusion
#        ext1 = extrudes.add(extInput)
        
    
    
    
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            
