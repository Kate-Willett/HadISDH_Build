; TIDL
; 
; Author: Kate Willett
; Created: 1 February 2013
; Last update: 15 January 2015
; Location: /data/local/hadkw/HADCRUH2/UPDATE2014/PROGS/HADISDH_BUILD/	
; GitHub: https://github.com/Kate-Willett/HadISDH_Build					
; -----------------------
; CODE PURPOSE AND OUTPUT
; -----------------------
; <brief summary of code purpose and main outputs>
; 
; <references to related published material, e.g. that describes data set>
; 
; -----------------------
; LIST OF MODULES
; -----------------------
; <List of program modules required to run the code, or link to compiler/batch file>
; 
; -----------------------
; DATA
; -----------------------
; <source data sets required for code; include data origin>
; 
; -----------------------
; HOW TO RUN THE CODE
; -----------------------
; <step by step guide to running the code>
; 
; -----------------------
; OUTPUT
; -----------------------
; <where this is written to and any other useful information about output>
; 
; -----------------------
; VERSION/RELEASE NOTES
; -----------------------
; 
; Version 1 (15 January 2015)
; ---------
;  
; Enhancements
;  
; Changes
;  
; Bug fixes
;  
; -----------------------
; OTHER INFORMATION
; -----------------------
;


;+
;      MAKE_KEY
;
; PURPOSE:
;      Create a color key for a plot.
;
;
; CALLING SEQUENCE:
;
;    MAKE_KEY,[[X,Y,XSIZE,YSIZE],[[XLABOFF,YLABOFF]]],COLORS=colors
;
;
; INPUTS:
;
;    No direct inputs required, except KEYWORD colors (see below).
;
;
; OUTPUTS:
;   A color key is drawn on the output device.
;
;
; OPTIONAL INPUT PARAMETERS:
;
;   X,Y:  x,y position of lower left corner of key.
;   XSIZE,YSIZE:  x,y size of key.
;       (If the above 4 are not supplied then optimal values are chosen.)
;
;   XLABOFF,YLABOFF:  x,y label offset (relative to lower left of box).
;       (If the above 2 are not supplied then optimal values are chosen.)
;
;	  All positions/sizes are in data coordinates, unless /NORMAL specified.
;
;
; KEYWORD PARAMETERS:
;
;   ALIGNMENT: label justification
;     (0=left (default for ORIENTATION=1), 0.5=center(default), 1=right)
;
;   BCOLOR: index (or scalar) of colors for border (default=!P.color)
;
;   BOXSIZE: the width of the boxes, in fractional units (i.e. 0.5,0.25,...)
;            This should be an (Nbox-1) vector, with TOTAL(BOXSIZE) < 1.
;            Default is 1.0/Nbox
;
;   CHARSIZE: size of labels (default=!P.charsize)
;
;   CHARTHICK: thickness of vector drawn characters (default=!P.charthick)
;
;   COLORS: array of Nbox colors for each box (this is required)
;
;   LABELS: array of strings for labels (can have 1 to Nbox+1 labels)
;
;   LINEANGLE: array of orientation angles of box fill lines
;
;   LINESPACING: array of line spacings (in cm) for box fill lines
;
;   NOBORDER: don't put a border around each box.
;
;   NORMAL: use normalized coordinates (default = data)
;
;   ORIENTATION: orientation of key:
;      (0=left to right (default), 1=top to bottom)
;
;   PATTERN: a MxMxNbox array of patterns, Nbox=index, MxM is pattern
;
;   THICK: thickness of border lines (default=!P.thick)
;
;   TITLE: a string to put below or next to the labels.
;
;   UNITS: a string used to label the topmost box (usually the data units)
;
;
;	   If LINESPACING or LINEANGLE are specified then line fills are done.
;	   If PATTERN is specified then pattern fills are done.
;	   Otherwise solid fills using COLORS are done.
;
;
;	   Number of boxes is determined from COLORS, LINE, or PATTERN.
;	   The number of labels (Nlab) is usually equal to or one more than Nbox.
;      If Nbox is an integer multiple of Nlab, then MAKE_KEY
;      will label every Nbox/Nlab box.
;
;
; EXAMPLE:
;
;   colors = [100,150,200,250]
;   levels = [0,1,2,3]
;   CONTOUR,DIST(20)/4,LEVELS=levels,C_COLOR=colors,/FILL,YMARGIN=[8,2]
; 	MAKE_KEY, COLORS=colors, LABELS=levels
;
;  ** Warning ** if you are on a map projection (from MAP_SET), then you need
;                to use NORMALized coordinates and specify all 6 parameters:
;
;        MAP_SET,/CONT,YMARGIN=[8,2]
;        MAKE_KEY,0.25,0.05,0.5,0.05,0,-0.03,/NORMAL, $
;            COLORS=[100,150,200,250], LABELS=[0,1,2,3]
;
;
; MODIFICATION HISTORY:
; Written, C. Torrence, Nov. 9, 1993.
; Modified, Frank Evans, CU, 2/24/94
; Modified, C. Torrence, July 1996. Changed INPUTS to optional.
; Fixed, C. Torrence, 1/13/99, MAP_SET proj require all 6 params in /NORMAL
;-
PRO MAKE_KEY,x,y,xsize,ysize,xlaboff,ylaboff, $
	COLORS=colors, LABELS=labels, UNITS=units, ORIENTATION=orientation, $
	NOBORDER=noborder, BCOLOR=bcolor, THICK=thick, NORMAL=normal,$
	PATTERN=pattern, LINESPACING=linespacing, LINEANGLE=lineangle, $
	ALIGNMENT=alignment, CHARSIZE=charsize, CHARTHICK=charthick, $
	TITLE=title,STEPLAB=steplab,BOXSIZE=boxsize,ARROW=arrow

	ON_ERROR,2  ;return to caller if error

	IF ((N_PARAMS(0) NE 0) AND (N_PARAMS(0) NE 4) AND (N_PARAMS(0) NE 6)) THEN $
		MESSAGE,"You supplied " + STRCOMPRESS(N_PARAMS(0),/REMOVE) + $
			" parameters. Needs 0, 4, or 6 parameters."

;*********************************************************** check KEYWORDS
	nbox = N_ELEMENTS(colors)
	ON_ERROR,2

	IF (nbox LT 1) THEN MESSAGE,'must have at least 1 color'
	patflag = (N_ELEMENTS(pattern) GT 0)
	IF patflag THEN BEGIN
		tmp = SIZE(pattern)
		IF tmp(0) EQ 3 THEN nbox = tmp(3)
	ENDIF

	lineflag = (N_ELEMENTS(linespacing) GT 0) OR (N_ELEMENTS(lineangle) GT 0)
	if lineflag THEN nbox = N_ELEMENTS(lineangle) < N_ELEMENTS(linespacing)
	IF NOT lineflag THEN BEGIN
		lineangle=INTARR(nbox)
		linespacing=INTARR(nbox)
	ENDIF

	IF nbox EQ 0 THEN MESSAGE, 'MAKEKEY: No boxes specified.'

	IF N_ELEMENTS(labels) LE 0 THEN labels=REPLICATE(nbox,'')
	s = SIZE(labels)
	IF (s(s(0) + 1) NE 7) THEN labels = STRTRIM(labels,2)
	nlab = N_ELEMENTS(labels)
	IF (N_ELEMENTS(steplab) LT 1) THEN steplab = FIX((nbox+1)/nlab) > 1

	noborder = KEYWORD_SET(noborder)
	orientation = KEYWORD_SET(orientation)
	normal = KEYWORD_SET(normal)
	IF N_ELEMENTS(bcolor) LE 0 THEN bcolor = !P.COLOR
	IF N_ELEMENTS(bcolor) EQ 1 THEN bcolor = BYTARR(nbox) + bcolor
	IF N_ELEMENTS(charsize) LE 0 THEN charsize = !P.CHARSIZE
	IF (charsize EQ 0) THEN charsize = 1
	IF N_ELEMENTS(thick) LE 0 THEN thick = !P.THICK
	IF N_ELEMENTS(charthick) LE 0 THEN charthick = !P.CHARTHICK

	IF (!MAP.PROJECTION GT 0) THEN BEGIN   ; be careful with MAP_SET
		IF (N_PARAMS(0) LT 6) THEN BEGIN
			MESSAGE,'For map projections you need ' + $
				'to supply all 6 parameters in NORMAL coordinates'
			RETURN
		ENDIF
		max_size = MAX(ABS([x,y,xsize,ysize,xlaboff,ylaboff]))
		IF (NOT normal) THEN BEGIN
			IF (max_size GT 2) THEN BEGIN
				MESSAGE,'For map projections you need ' +$
					'to use NORMAL coordinates'
				RETURN
			ENDIF
			normal = 1
			MESSAGE,/INFO,'** Warning** assuming /NORMAL coordinates'
		ENDIF
	ENDIF

;**************************************** check how many parameters supplied

	IF (N_PARAMS(0) EQ 0) THEN BEGIN   ;****** need to create all parameters
		zero = CONVERT_COORD(0,0,/DEVICE,/TO_DATA)
		zero_data = CONVERT_COORD(0,0,/DATA,/TO_NORMAL)
		char_size = CONVERT_COORD(!D.X_CH_SIZE,!D.Y_CH_SIZE,/DEVICE,/TO_DATA)
		char_size = (char_size - zero)*charsize
		IF (orientation) THEN BEGIN   ; vertical
			x = !X.CRANGE(1) + 1.5*char_size(0) ;*(!P.CHARSIZE/charsize)
			y = !Y.CRANGE(0)
			xsize = 1.5*char_size(0)
			ysize = !Y.CRANGE(1) - !Y.CRANGE(0)
		ENDIF ELSE BEGIN   ; horizontal
			x = !X.CRANGE(0)
			y = !Y.CRANGE(0) - 5.5*char_size(1) ;*(!P.CHARSIZE/charsize)
			xsize = !X.CRANGE(1) - !X.CRANGE(0)
			ysize = 1.5*char_size(1)
		ENDELSE
		IF normal THEN BEGIN
			dummy = CONVERT_COORD([x,xsize],[y,ysize],/DATA,/TO_NORMAL)
			x = dummy(0,0)
			y = dummy(1,0)
			xsize = dummy(0,1) - zero_data(0)
			ysize = dummy(1,1) - zero_data(1)
		ENDIF
	ENDIF

	IF N_PARAMS(0) LT 6 THEN BEGIN   ;****** need to supply label offsets
		zero = CONVERT_COORD(0,0,/DEVICE,/TO_DATA)
		zero_data = CONVERT_COORD(0,0,/DATA,/TO_NORMAL)
		char_size = CONVERT_COORD(!D.X_CH_SIZE,!D.Y_CH_SIZE,/DEVICE,/TO_DATA)
		char_size = (char_size - zero)*charsize
		IF orientation THEN BEGIN   ; vertical
			xlaboff = 0.6*char_size(0)
			ylaboff = -0.4*char_size(1)
		ENDIF ELSE BEGIN   ; horizontal
			xlaboff = 0.
			ylaboff = -1.4*char_size(1)
		ENDELSE
		IF normal THEN BEGIN
			dummy = CONVERT_COORD(xlaboff,ylaboff,/DATA,/TO_NORMAL)
			xlaboff = dummy(0) - zero_data(0)
			ylaboff = dummy(1) - zero_data(1)
		ENDIF
		xlaboff = xlaboff + xsize*orientation   ;* add in KEY width if vertical
	ENDIF


;**************************************************** create POLYFILL arrays
	zeros = FLTARR(nbox+1)
	IF orientation THEN BEGIN   ;*********** vertical
		xbox = zeros + xsize
		ybox = zeros + FLOAT(ysize)/nbox
		IF (N_ELEMENTS(boxsize) GE nbox-1) THEN $
			ybox = [boxsize*FLOAT(ysize),ysize-TOTAL(boxsize)]
		x = zeros + x
		y = zeros + y
		FOR i=1,nbox DO y(i) = y(i-1) + ybox(i-1)
		IF N_ELEMENTS(alignment) LE 0 THEN alignment = 0
	ENDIF ELSE BEGIN   ;*********** horizontal
		xbox = zeros + FLOAT(xsize)/nbox
		ybox = zeros + ysize
		IF (N_ELEMENTS(boxsize) GE nbox-1) THEN $
			xbox = [boxsize*FLOAT(xsize),xsize*(1.-TOTAL(boxsize))]
		y = zeros + y
		x = zeros + x
		FOR i=1,nbox DO x(i) = x(i-1) + xbox(i-1)
		IF N_ELEMENTS(alignment) LE 0 THEN alignment = 0.5
	ENDELSE


;********************  Make the boxes and draw lines around them (if desired)
	FOR i = 0, nbox-1 DO BEGIN
		IF KEYWORD_SET(arrow) AND (i EQ 0 or i EQ nbox-1) THEN BEGIN
		  IF ORIENTATION eq 0 AND i eq 0 THEN BEGIN
			xx=[x(i),x(i)+xbox(i),x(i)+xbox(i),x(i)]
			yy=[y(i)+ybox(i)/2,y(i),y(i)+ybox(i),y(i)+ybox(i)/2]
		  ENDIF ELSE IF ORIENTATION eq 1 and i eq 0 THEN BEGIN
			xx=[x(i),x(i)+xbox(i),x(i)+xbox(i)/2,x(i)]
			yy=[y(i)+ybox(i),y(i)+ybox(i),y(i),y(i)+ybox(i)]
		  ENDIF ELSE IF ORIENTATION eq 0 AND i EQ nbox-1 THEN BEGIN
            xx=[x(i),x(i)+xbox(i),x(i),x(i)]
            yy=[y(i),y(i)+ybox(i)/2,y(i)+ybox(i),y(i)]
          ENDIF ELSE IF ORIENTATION eq 1 AND i EQ nbox-1 THEN BEGIN
            xx=[x(i),x(i)+xbox(i),x(i)+xbox(i)/2,x(i)]
            yy=[y(i),y(i),y(i)+ybox(i),y(i)]
		  ENDIF
		ENDIF ELSE BEGIN
			xx=[x(i),x(i)+xbox(i),x(i)+xbox(i),x(i)]
			yy=[y(i),y(i),y(i)+ybox(i),y(i)+ybox(i)]
		ENDELSE
		IF patflag THEN POLYFILL,xx,yy,NORMAL=normal,PATTERN=pattern(*,*,i) $
		ELSE IF linespacing(i) THEN POLYFILL,xx,yy, NORMAL=normal, $
			/LINE_FILL, SPACING=linespacing(i), $
			ORIENTATION=lineangle(i), COLOR=colors(i) $
		ELSE POLYFILL,xx,yy, NORMAL=normal,COLOR=colors(i)
		IF noborder EQ 0 THEN PLOTS,[xx,x(i)],[yy,y(i)], normal=normal, $
			COLOR=bcolor(i), /NOCLIP,THICK=thick
;		IF KEYWORD_SET(arrow) and orientation EQ 0 THEN $
;			PLOTS,[x(0),x(0)],[y(0),y(0)+ybox(0)/2],$
;				  COLOR=255, /NOCLIP,THICK=thick+1
	ENDFOR
;print,bcolor
;***********************************************************  Label the boxes
	FOR i = 0, nlab-1 DO BEGIN
		XYOUTS,x(i*steplab) + xlaboff,y(i*steplab) + ylaboff, $
			labels(i), NORMAL=normal,ALIGNMENT=alignment, $
			CHARSIZE=charsize,CHARTHICK=charthick,color=0
	ENDFOR

	IF ((N_ELEMENTS(units) GT 0) AND ((nlab-1)*steplab NE nbox)) THEN BEGIN
		XYOUTS,x(nbox) + xlaboff,y(nbox) + ylaboff, $
			units, NORMAL=normal,ALIGNMENT=alignment, $
			CHARSIZE=charsize, CHARTHICK=charthick
	ENDIF ;** units
	
	IF (N_ELEMENTS(title) GT 0) THEN BEGIN
		IF orientation THEN BEGIN
			x_title = x(0) + xlaboff + 0.6*xsize*(MAX(STRLEN(labels)) + 1)
			y_title = y(0) + ysize/2.
		ENDIF ELSE BEGIN
			x_title =x(0) + xsize/2.
print,x_title
			y_title = y(0) + ylaboff - 0.9*ysize 
print,y_title	
	ENDELSE
	;	XYOUTS,x_title,y_title,title,ORIENTATION=-90*orientation, $
		;	ALIGNMENT=0.5,CHARTHICK=charthick,CHARSIZE=charsize,color=colors(1)
	XYOUTS,x_title,y_title,title
ENDIF

END

