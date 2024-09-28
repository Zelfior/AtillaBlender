fn readFixedString file len =
(
   local str = ""

   for i = 1 to len do
   (
      str0 = readByte file #unsigned
      if str0 != 0xFD AND str0 != 0xFC do str += bit.intAsChar str0
   )
   
   str
)

fn toMeters unitVal = -- converts the value in unitVal into meters, taking into account the current system units
(
	scaleFactor = units.decodeValue "1m" -- this many system units make up one meter
	unitVal * scaleFactor
)

struct Vec2
(
	x,
	y,
	
	fn read file =
	(
		x  = toMeters (readFloat file)
		y  = toMeters (readFloat file)
	)
)

struct Vec3
(
	x,
	y,
	z,
	
	fn read file =
	(
		x  = toMeters (readFloat file)
		y  = toMeters (readFloat file)
		z  = toMeters (readFloat file)
	)
)

struct BoundingBox
(
	minX,
	minY,
	minZ,
	maxX,
	maxY,
	maxZ,
	
	fn read file =
	(
		minX = readFloat file
		minY = readFloat file
		minZ = readFloat file
		minX = readFloat file
		minY = readFloat file
		minZ = readFloat file
	)
)

struct UnicodeString
(
	strLen,
	str,
	
    fn read file =
    (
		strLen = readShort file
		str = readFixedString file (strLen * 2)
		--print str
	)
)

struct TransformMatrix
(
	row0_col0,
	row1_col0,
	row2_col0,
	row3_col0,
	row0_col1,
	row1_col1,
	row2_col1,
	row3_col1,
	row0_col2,
	row1_col2,
	row2_col2,
	row3_col2,
	row0_col3,
	row1_col3,
	row2_col3,
	row3_col3,
	
    fn read file =
    (
		row0_col0 = readFloat file
		row0_col1 = readFloat file
		row0_col2 = readFloat file
		row0_col3 = readFloat file
		row1_col0 = readFloat file
		row1_col1 = readFloat file
		row1_col2 = readFloat file
		row1_col3 = readFloat file
		row2_col0 = readFloat file
		row2_col1 = readFloat file
		row2_col2 = readFloat file
		row2_col3 = readFloat file
		row3_col0 = toMeters (readFloat file)
		row3_col1 = toMeters (readFloat file)
		row3_col2 = toMeters (readFloat file)
		row3_col3 = readFloat file
	),
	
	fn getMatrix =
	(
		local matrix = matrix3 [row0_col0, row0_col1, row0_col2] [row1_col0, row1_col1, row1_col2] [row2_col0, row2_col1, row2_col2] [row3_col0, row3_col2, row3_col1]
		
		matrix
	)
)

struct TechNode
(
	nodeName,
	nodeTransform,
	
	fn read file =
	(
		nodeName = UnicodeString()
		nodeTransform = TransformMatrix()
		
		nodeName.read file
		nodeTransform.read file
	),
	
	fn create =
	(
		if nodeName.str == undefined or nodeName.str == "" do
		(
			return 0
		)
		
		local isArrowEmitter = findString nodeName.str "arrow_emitter" != undefined
		local isDockingPoint = findString nodeName.str "docking_point" != undefined
		local isActionVFX = findString nodeName.str "action_vfx" != undefined
		local isCannon = findString nodeName.str "cannon" != undefined
		
		if isArrowEmitter then
		(
			vertices = #([-11.8767,-11.6213,0], [11.8767,-11.6213,0], [-11.8767,11.6213,0], [11.8767,11.6213,0], [0, 0, -4.08661])
			normals = #([0,0,1], [0,0,1], [0,-0.331736,-0.943372], [0.325364,0,-0.945589], [0,0.331736,-0.943372], [-0.325364,0,-0.945589])
			indices = #([1,3,4], [4,2,1], [1,2,5], [2,4,5], [4,3,5], [3,1,5])
			
			m = mesh vertices:vertices faces:indices
			m.name = nodeName.str
			m.transform = nodeTransform.getMatrix()
			m.wirecolor = color 225 198 87
			
			convertToPoly m
			select m
			subobjectLevel = 4
			m.EditablePoly.SetSelection #Face #{1..6}
			m.autoSmoothThreshold = 15
			m.EditablePoly.autosmooth ()
			macros.run "Editable Polygon Object" "EPoly_Flip"
			subobjectLevel = 0
			deselect m
		)
		--else if isDockingPoint then
		--(
			-- TODO
		--)
		--else if isActionVFX then
		--(
			-- TODO
		--)
		else
		(
			m = box length:(toMeters 1) width:(toMeters 1) height:(toMeters 1)
			m.name = nodeName.str
			m.transform = nodeTransform.getMatrix()
			m.wirecolor = color 28 149 177
		)
	)
)

struct FaceEdge
(
	vertexIndex0,
	vertexIndex1,
	edgeIndex,
	unknown,
	
	fn read file =
	(
		vertexIndex0 = readLong file
		vertexIndex1 = readLong file
		edgeIndex = readLong file
		unknown = readLong file
	)
)

struct FaceEdgeData
(
	edge0,
	edge1,
	edge2,
	edge3,
	
	fn read file =
	(
		edge0 = FaceEdge()
		edge0.read file
		
		edge1 = FaceEdge()
		edge1.read file
		
		edge2 = FaceEdge()
		edge2.read file
		
		edge3 = FaceEdge()
		edge3.read file
	)
)

struct Face
(
	faceIndex,
	vertIndex0,
	vertIndex1,
	vertIndex2,
	edgeData,
	
	fn read file = 
	(
		faceIndex = readLong file
		local padding = readByte file
		vertIndex0 = readLong file
		vertIndex1 = readLong file
		vertIndex2 = readLong file
		
		edgeData = FaceEdgeData()
		edgeData.read file
	)
)

struct Collision3D
(
	collisionName,
	nodeIndex,
	unknown2,
	numVerts,
	dataVerts,
	numFaces,
	dataFaces,
	
	fn read file =
	(
		collisionName = UnicodeString()
		collisionName.read file
		
		nodeIndex = readLong file
		unknown2 = readLong file
		numVerts = readLong file
		
		dataVerts = #()
		for i = 1 to numVerts do
		(
			local vert = Vec3()
			vert.read file
			append dataVerts [vert.x, vert.z, vert.y]
		)
		
		numFaces = readLong file
		dataFaces = #()
		for i = 1 to numFaces do
		(
			local newFace = Face()
			newFace.read file
			append dataFaces [newFace.vertIndex0+1, newFace.vertIndex2+1, newFace.vertIndex1+1]
		)
	),
	
	fn create =
	(
		if numVerts == 0 do
		(
			return 0
		)
		
		m = mesh vertices:dataVerts faces:dataFaces
		m.name = collisionName.str
		m.wirecolor = color 135 6 6
	)
)

struct LineNode
(
	lineName,
	numVerts,
	dataVerts,
	lineType,
	
	fn read file =
	(
		lineName = UnicodeString()
		lineName.read file
		
		dataVerts = #()
		numVerts = readLong file
		for i = 1 to numVerts do
		(
			local vert = Vec3()
			vert.read file
			append dataVerts [vert.x, vert.z, vert.y]
		)
		
		lineType = readLong file
	),
	
	fn create _close =
	(
		if numVerts == 0 do
		(
			return 0
		)
		
		local lineColor = color 176 26 26
		local isGroundAd = findString lineName.str "ground_ad" != undefined
		local isHard = findString lineName.str "hard" != undefined
		local isPipe = findString lineName.str "pipe" != undefined
		
		if isGroundAd then
		(
			lineColor = color 225 198 87
		)
		else if isHard then
		(
			lineColor = color 255 255 255
		)
		else if isPipe then
		(
			lineColor = color 166 229 229
		)
		
		local newLine = line name:lineName.str
		newLine.wirecolor = lineColor
		addnewspline newLine
		
		for vert in dataVerts do
		(
			addKnot newLine 1 #corner #line vert
		)
		
		if _close then
		(
			close newLine 1
		)
		
		updateShape newLine
	)
)

struct NogoZone
(
	numLines,
	dataLines,
	
	fn read file = 
	(
		numLines = readLong file
		for i = 1 to numLines do
		(
			local vert = Vec2()
			vert.read file
			local numLinesConnected = readLong file
		)
	)
)

struct Polygon
(
	normal,
	numVerts,
	dataVerts,
	isPlatformGround,
	
	fn read file = 
	(
		normal = Vec3()
		normal.read file
		
		dataVerts = #()
		numVerts = readLong file
		for i = 1 to numVerts do
		(
			local vert = Vec3()
			vert.read file
			append dataVerts [vert.x, vert.z, vert.y]
		)
		
		local flag1 = readByte file
		isPlatformGround = (readByte file) != 0
		local flag3 = readByte file
	)
)

struct Platform
(
	numPolygons,
	dataPolygons,
	
	fn read file =
	(
		numPolygons = readLong file
		
		dataPolygons = #()
		for i = 1 to numPolygons do
		(
			local _polygon = Polygon()
			_polygon.read file
			append dataPolygons _polygon
		)
		
		-- parent node index?
		local unknown = readLong file
	),
	
	fn create destructName =
	(
		if numPolygons == 0 do
		(
			return 0
		)
		
		local platformPolygons = #()
		local groundPolygons = #()
		
		for i = 1 to numPolygons do
		(
			local polygon = dataPolygons[i]
			
			local m = line name:"temp"
			addnewspline m
			
			for vert in polygon.dataVerts do
			(
				addKnot m 1 #corner #line vert
			)
			
			close m 1
			convertToPoly m
			
			if polygon.isPlatformGround then
			(
				append groundPolygons m
			)
			else
			(
				append platformPolygons m
			)
		)
		
		if platformPolygons.count > 0 do
		(
			local nameStream = stringStream ""
			format "%_platform01" destructName to:nameStream
			local platformName = nameStream as string
			
			platformMesh = mesh name:platformName vertices:#() faces:#()
			platformMesh.wirecolor = color 115 115 115
			
			for m in platformPolygons do
			(
				attach platformMesh m
			)
			
			convertToPoly platformMesh
			select platformMesh
			
			platformMesh.EditablePoly.SetSelection #Vertex #{1..(platformMesh.verts.count)}
			platformMesh.weldThreshold = 0.01
			platformMesh.EditablePoly.weldFlaggedVertices ()
			platformMesh.EditablePoly.SetSelection #Vertex #{1..1}
			
			deselect platformMesh
			update platformMesh
		)
		
		if groundPolygons.count > 0 do
		(
			local nameStream = stringStream ""
			format "%_platform_ground" destructName to:nameStream
			local groundName = nameStream as string
			
			groundMesh = mesh name:groundName vertices:#() faces:#()
			groundMesh.wirecolor = color 6 135 113
			
			for m in groundPolygons do
			(
				attach groundMesh m
			)
			
			convertToPoly groundMesh
			select groundMesh
			
			groundMesh.EditablePoly.SetSelection #Vertex #{1..(groundMesh.verts.count)}
			groundMesh.weldThreshold = 0.01
			groundMesh.EditablePoly.weldFlaggedVertices ()
			groundMesh.EditablePoly.SetSelection #Vertex #{1..1}
			
			deselect groundMesh
			update groundMesh
		)
	)
)

struct SoftCollision
(
	nodeName,
	nodeTransform,
	cylinderRadius,
	cylinderHeight,
	
	fn read file =
	(
		nodeName = UnicodeString()
		nodeName.read file
		
		nodeTransform = TransformMatrix()
		nodeTransform.read file
		
		local unknown = readShort file
		cylinderRadius = toMeters(readFloat file)
		cylinderHeight = toMeters(readFloat file)
	),
	
	fn create =
	(
		if nodeName.str == undefined or nodeName.str == "" do
		(
			return 0
		)
		
		m = cylinder radius:cylinderRadius height:cylinderHeight sides:5 heightSegs:1
		m.name = nodeName.str
		m.transform = nodeTransform.getMatrix()
		m.wirecolor = color 255 198 87
	)
)

struct FileRef
(
	fileKey,
	fileName,
	fileTransform,
	
	fn read file =
	(
		fileKey = UnicodeString()
		fileKey.read file
		
		fileName = UnicodeString()
		fileName.read file
		
		fileTransform = TransformMatrix()
		fileTransform.read file
		
		local unknown = readShort file
	),
	
	fn create =
	(
		if fileKey.str == undefined or fileKey.str == "" do
		(
			return 0
		)
		
		local newBox = box length:(toMeters 1) width:(toMeters 1) height:(toMeters 1)
		newBox.name = fileKey.str
		newBox.transform = fileTransform.getMatrix()
		newBox.wirecolor = color 255 255 255
	)
)

struct EFLine
(
	lineName,
	lineAction,
	lineStart,
	lineEnd,
	lineDir,
	parentIndex,
	
	fn read file =
	(
		lineName = UnicodeString()
		lineName.read file
		
		-- TODO: finish
		lineAction = readLong file
		
		lineStart = Vec3()
		lineStart.read file
		
		lineEnd = Vec3()
		lineEnd.read file
		
		lineDir = Vec3()
		lineDir.read file
		
		parentIndex = readLong file
	),
	
	fn create =
	(
		if lineName.str == undefined or lineName == "" do
		(
			return 0
		)
		
		local newLine = line name:lineName.str
		newLine.wirecolor = color 225 198 87
		addnewspline newLine
		
		addKnot newLine 1 #corner #line [lineStart.x, lineStart.z, lineStart.y]
		addKnot newLine 1 #corner #line [lineEnd.x, lineEnd.z, lineEnd.y]
		
		updateShape newLine
	)
)

struct VFXAttachment
(
	numIndices,
	dataIndices,
	
	fn read file =
	(
		dataIndices = #()
		numIndices = readLong file
		for i = 1 to numIndices do
		(
			local index = readShort file
			append dataIndices index
		)
	)
)

struct DestructLevel
(
	destructName,
	destructIndex,
	collision3dMesh,
	numWindows,
	collision3dWindows,
	numDoors,
	collision3dDoors,
	numSpecial,
	collision3dSpecial,
	numLines,
	dataLines,
	numPipes,
	dataPipes,
	platforms,
	numCannons,
	dataCannons,
	numArrowEmitters,
	dataArrowEmitters,
	numDockingPoints,
	dataDockingPoints,
	numSoftCollisions,
	dataSoftCollisions,
	numFileRefs,
	dataFileRefs,
	numEFLines,
	dataEFLines,
	
	fn read file version = 
	(
		collision3dWindows = #()
		collision3dDoors = #()
		collision3dSpecial = #()
		
		destructName = UnicodeString()
		destructName.read file
		
		destructIndex = readLong file
		
		collision3dMesh = Collision3D()
		collision3dMesh.read file
		collision3dMesh.create()
		
		numWindows = readLong file
		for i = 1 to numWindows do
		(
			collision3dWindow = Collision3D()
			collision3dWindow.read file
			collision3dWindow.create()
			append collision3dWindows collision3dWindow
		)
		
		numDoors = readLong file
		for i = 1 to numDoors do
		(
			collision3dDoor = Collision3D()
			collision3dDoor.read file
			collision3dDoor.create()
			append collision3dDoors collision3dDoor
		)
		
		numSpecial = readLong file
		for i = 1 to numSpecial do
		(
			local firstCollision3D = Collision3D()
			firstCollision3D.read file
			firstCollision3D.create()
			append collision3dSpecial firstCollision3D
			
			local secondCollision3D = Collision3D()
			secondCollision3D.read file
			secondCollision3D.create()
			append collision3dSpecial secondCollision3D
		)
		
		dataLines = #()
		numLines = readLong file
		for i = 1 to numLines do
		(
			local newLine = LineNode()
			newLine.read file
			newLine.create(true)
			
			append dataLines newLine
		)
		
		dataPipes = #()
		numPipes = readLong file
		for i = 1 to numPipes do
		(
			local newPipe = LineNode()
			newPipe.read file
			newPipe.create(false)
			
			append dataPipes newPipe
		)
		
		local numNogo = readLong file
		for i = 1 to numNogo do
		(
			local nogo = NogoZone()
			nogo.read file
		)
		
		platforms = Platform()
		platforms.read file
		platforms.create destructName.str
		
		-- Read destruct bounding box
        local bbox = BoundingBox()
		bbox.read file
		
		dataCannons = #()
		numCannons = readLong file
		for i = 1 to numCannons do
		(
			local cannon = TechNode()
			cannon.read file
			append dataCannons cannon
			cannon.create()
		)
		
		dataArrowEmitters = #()
		numArrowEmitters = readLong file
		for i = 1 to numArrowEmitters do
		(
			local arrowEmitter = TechNode()
			arrowEmitter.read file
			append dataArrowEmitters arrowEmitter
			arrowEmitter.create()
		)
		
		dataDockingPoints = #()
		numDockingPoints = readLong file
		for i = 1 to numDockingPoints do
		(
			local dockingPoint = TechNode()
			dockingPoint.read file
			append dataDockingPoints dockingPoint
			dockingPoint.create()
		)
		
		dataSoftCollisions = #()
		numSoftCollisions = readLong file
		for i = 1 to numSoftCollisions do
		(
			local _softCollision = SoftCollision()
			_softCollision.read file
			append dataSoftCollisions _softCollision
			_softCollision.create()
		)
		
		-- Unknown array
		local arraySize = readLong file
		if arraySize > 0 do
		(
			print "Unknown array detected at " + (ftell file) + "! Aborting.."
			fclose file
			exit()
		)
		
		dataFileRefs = #()
		numFileRefs = readLong file
		for i = 1 to numFileRefs do
		(
			local ref = FileRef()
			ref.read file
			append dataFileRefs ref
			ref.create()
		)
		
		dataEFLines = #()
		numEFLines = readLong file
		for i = 1 to numEFLines do
		(
			local ef_line = EFLine()
			ef_line.read file
			append dataEFLines ef_line
			ef_line.create()
		)
		
		arraySize = readLong file
		if arraySize > 0 do
		(
			print "Unknown array detected at " + (ftell file) + "! Aborting.."
			fclose file
			exit()
		)
		
		if version == 11 do
		(
			return 0
		)
		
		local numActionVFX = readLong file
		for i = 1 to numActionVFX do
		(
			local actionVFX = TechNode()
			actionVFX.read file
		)
		
		local numSecondActionVFX = readLong file
		for i = 1 to numSecondActionVFX do
		(
			local actionVFX = TechNode()
			actionVFX.read file
		)
		
		local numAttActionVFX = readLong file
		for i = 1 to numAttActionVFX do
		(
			local attActionVFX = VFXAttachment()
			attActionVFX.read file
		)
		
		local numSecondAttActionVFX = readLong file
		for i = 1 to numSecondAttActionVFX do
		(
			local attActionVFX = VFXAttachment()
			attActionVFX.read file
		)
	)
)

struct BuildingPiece
(
	pieceName,
	placementNode,
	parentIndex,
	destructCount,
	destructs,	
	
    fn read file version =
    (
		pieceName = UnicodeString()
		pieceName.read file
		
		placementNode = TechNode()
		placementNode.read file
		
		parentIndex = readLong file
		destructCount = readLong file
		
		destructs = #()
		for i = 1 to destructCount do
		(
			local destruct = DestructLevel()
			destruct.read file version
			append destructs destruct
		)
		
		local arraySize = readLong file
		if arraySize > 0 do
		(
			print "Unknown array detected at " + (ftell file) + "! Aborting.."
			fclose file
			exit()
		)
	)
)

rollout unnamedRollout "Untitled" width:170 height:124
(
	button 'btn1' "Open" pos:[11,45] width:129 height:52 align:#left
	
	on btn1 pressed do
	(
		local filePath = getOpenFileName caption:"Select a file" types:"Building Tech Files (*.cs2.parsed)|*.cs2.parsed"
		if filePath == undefined or filePath == "" do
		(
			return 0
		)
		
		local file = fopen filePath "rb"
		if file == undefined do
		(
			return 0
		)
		
		-- Read file version
		local version = ReadLong file
		if version != 13 and version != 11 do
		(
			print "Unsupported .cs2.parsed file version!"
			fclose file
			exit()
		)
		
		-- Read building bounding box
        local bbox = BoundingBox()
		bbox.read file
		
		-- Read UI flag
		local flag = TechNode()
		flag.read file
		flag.create()
		
		-- Unknown array
		local arraySize = readLong file
		if arraySize > 0 do
		(
			print "Unknown array detected at " + (ftell file) + "! Aborting.."
			fclose file
			exit()
		)
		
		-- Pieces array
		local pieceCount = readLong file
		for i = 1 to pieceCount do
		(
			local piece = BuildingPiece()
			piece.read file version
		)
		
		fclose file
		
		local zoneFilePath = substring filePath 1 (filePath.count - 15)
		zoneFilePath = zoneFilePath + "zone_tech.xml"
		if zoneFilePath == undefined or zoneFilePath == "" do
		(
			fclose file
			return 0
		)
		
		if not doesFileExist zoneFilePath do
		(
			fclose file
			return 0
		)
		
		print zoneFilePath
	)
)

createDialog unnamedRollout