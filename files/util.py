def extension_is(path, extension):
	'''Returns true if the file's extension is the same as the extension passed'''
	return path[-3:] == extension

def with_extension(path, extension):
	'''Returns the file path with its extension replaced with the extension passed'''
	return path[:-3] + extension