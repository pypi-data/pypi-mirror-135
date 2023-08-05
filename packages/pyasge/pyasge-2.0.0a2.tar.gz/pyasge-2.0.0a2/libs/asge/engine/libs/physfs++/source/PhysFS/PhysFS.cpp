#include <cstring>
#include "PhysFS.hpp"

std::string PhysFS::getBaseDir()
{
	return PHYSFS_getBaseDir();
}

std::string PhysFS::getPrefDir(const std::string& org_name, const std::string& app_name)
{
    return PHYSFS_getPrefDir(org_name.c_str(), app_name.c_str());
}


std::string PhysFS::getWriteDir()
{
	return PHYSFS_getWriteDir();
}

PhysFS::Version
PhysFS::getLinkedVersion() noexcept
{
	return Version();
}

PhysFS::IOResult
PhysFS::init(char const* argv0) noexcept
{
	return PHYSFS_init(argv0) != 0
		? IOResult::PHYSFS_OK : IOResult::PHYSFS_ERROR;
}

PhysFS::IOResult
PhysFS::deinit() noexcept
{
	return PHYSFS_deinit() != 0
		? IOResult::PHYSFS_OK : IOResult::PHYSFS_ERROR;
}

PhysFS::ArchiveInfoList
PhysFS::supportedArchiveTypes()
{
	ArchiveInfoList types;
	const auto physfs_types = PHYSFS_supportedArchiveTypes();
	for (const ArchiveInfo** info = physfs_types; *info != nullptr; ++info)
	{
		types.push_back(**info);
	}

	return types;
}

std::string PhysFS::getDirSeparator()
{
	return PHYSFS_getDirSeparator();
}

void PhysFS::permitSymbolicLinks(bool allow) noexcept
{
	PHYSFS_permitSymbolicLinks(allow);
	return;
}

PhysFS::StringList
PhysFS::getCdRomDirs()
{
	StringList available_drives;
	auto physfs_drives = PHYSFS_getCdRomDirs();
	for (char** drive = physfs_drives; *drive != nullptr; ++drive)
	{
		available_drives.push_back(*drive);
	}

	PHYSFS_freeList(physfs_drives);
	return available_drives;
}

void PhysFS::getCdRomDirs(StringCallback callback, void * extra) noexcept
{
	PHYSFS_getCdRomDirsCallback(callback, extra);
}

PhysFS::IOResult PhysFS::setWriteDir(const std::string& new_dir) noexcept
{
	return
	PHYSFS_setWriteDir(new_dir.c_str())
	? IOResult::PHYSFS_OK : IOResult::PHYSFS_ERROR;
}

void PhysFS::unmount(const std::string& old_dir) noexcept
{
	PHYSFS_unmount(old_dir.c_str());
}

PhysFS::StringList
PhysFS::getSearchPath()
{
	StringList physfs_paths;
	auto search_paths = PHYSFS_getSearchPath();
	for (char** path = search_paths; *path != nullptr; ++path)
	{
		physfs_paths.push_back(*path);
	}

	PHYSFS_freeList(search_paths);
	return physfs_paths;
}

void PhysFS::getSearchPath(PhysFS::StringCallback callback, void* data) noexcept
{
	PHYSFS_getSearchPathCallback(callback, data);
}

void PhysFS::setSaneConfig(
	const std::string& org_name, const std::string& game_name, const std::string& archive_ext,
	bool include_cdroms, bool archives_first) noexcept
{
	PHYSFS_setSaneConfig(org_name.c_str(), game_name.c_str(), archive_ext.c_str(), include_cdroms, archives_first);
}

int PhysFS::mkdir(const std::string& dir_name) noexcept
{
	return PHYSFS_mkdir(dir_name.c_str());
}

int PhysFS::deleteFile(const std::string& filename) noexcept
{
	return PHYSFS_delete(filename.c_str());
}

std::string PhysFS::getRealDir(const std::string& filename)
{
	return PHYSFS_getRealDir(filename.c_str());
}

PhysFS::StringList
PhysFS::enumerateFiles(const std::string& directory) noexcept
{
	StringList dirs;

	auto physfs_dirs = PHYSFS_enumerateFiles(directory.c_str());
	for (char** path = physfs_dirs; *path != nullptr; ++path)
	{
		dirs.push_back(*path);
	}

	PHYSFS_freeList(physfs_dirs);
	return dirs;
}

void PhysFS::enumerateFiles(const std::string& directory, EnumFilesCallback callback, void* data) noexcept
{
	PHYSFS_enumerate(directory.c_str(), callback, data);
}

bool PhysFS::exists(const std::string& filename) noexcept
{
	return PHYSFS_exists(filename.c_str());
}

PhysFS::MetaData
PhysFS::getMetaData(const std::string& filename) noexcept
{
	MetaData meta;
	PHYSFS_stat(filename.c_str(), &meta);
	return meta;
}

bool PhysFS::isDirectory(const std::string& filename) noexcept
{
	return getMetaData(filename).filetype == FileType::PHYSFS_FILETYPE_DIRECTORY;
}

bool PhysFS::isSymbolicLink(const std::string& filename) noexcept
{
	return getMetaData(filename).filetype == FileType::PHYSFS_FILETYPE_SYMLINK;
}

PhysFS::sint64
PhysFS::getLastModTime(const std::string& filename) noexcept
{
	return getMetaData(filename).modtime;
}

bool PhysFS::isInititalised() noexcept
{
	return PHYSFS_isInit();
}

bool PhysFS::symbolicLinksPermitted() noexcept
{
	return PHYSFS_symbolicLinksPermitted();
}

PhysFS::IOResult
PhysFS::setAllocator(const Allocator* allocator) noexcept
{
	return
		PHYSFS_setAllocator(allocator) != 0
		? IOResult::PHYSFS_OK : IOResult::PHYSFS_ERROR;
}

PhysFS::IOResult
PhysFS::mount(const std::string& dir, const std::string& mount_point, bool append_to_path) noexcept
{
	return
		PHYSFS_mount(dir.c_str(), mount_point.c_str(), append_to_path) != 0
		? IOResult::PHYSFS_OK : IOResult::PHYSFS_ERROR;
}

PhysFS::FileIO_ErrorCode
PhysFS::getLastErrorCode() noexcept
{
	return PHYSFS_getLastErrorCode();
}

std::string PhysFS::getMountPoint(const std::string& dir)
{
	return PHYSFS_getMountPoint(dir.c_str());
}

PHYSFS_File *PhysFS::open(const std::string &file_name, PhysFS::IOMode mode)
{
	PHYSFS_File* handle;
	switch (mode)
	{
		case IOMode::READ:
			handle = PHYSFS_openRead(file_name.c_str());
			break;


		case IOMode::APPEND:
			handle = PHYSFS_openAppend(file_name.c_str());
			break;

		case IOMode::WRITE:
			handle = PHYSFS_openWrite(file_name.c_str());
			break;
	}

	return handle;
}

bool PhysFS::close(PHYSFS_File *file) noexcept
{
	if (!file)
	{
		return  true;
	}

	if (PHYSFS_close(file) == 1)
	{
		return true;
	}

	return false;
}

PhysFS::sint64 PhysFS::writeBytes(PHYSFS_File *handle, const void *buffer, PhysFS::uint64 length)
{
	if (handle)
	{
		return PHYSFS_writeBytes(handle, buffer, length);
	}

	return 0;
}

PhysFS::sint64 PhysFS::readBytes(PHYSFS_File *handle, void *buffer, PhysFS::uint64 length)
{
	return PHYSFS_readBytes(handle, buffer, length);
}

PhysFS::sint64 PhysFS::length(PHYSFS_File *handle)
{
	return PHYSFS_fileLength(handle);
}

int PhysFS::seek(PHYSFS_file *handle, PhysFS::uint64 pos)
{
	return PHYSFS_seek(handle, pos);
}


PhysFS::sint16
PhysFS::Util::swapSLE16(sint16 value) noexcept
{
	return PHYSFS_swapSLE16(value);
}

PhysFS::uint16
PhysFS::Util::swapULE16(uint16 value) noexcept
{
	return PHYSFS_swapULE16(value);
}

PhysFS::sint32
PhysFS::Util::swapSLE32(sint32 value) noexcept
{
	return PHYSFS_swapSLE32(value);
}

PhysFS::uint32
PhysFS::Util::swapULE32(uint32 value) noexcept
{
	return PHYSFS_swapULE32(value);
}

PhysFS::sint64
PhysFS::Util::swapSLE64(sint64 value) noexcept
{
	return PHYSFS_swapSLE64(value);
}

PhysFS::uint64
PhysFS::Util::swapULE64(uint64 value) noexcept
{
	return PHYSFS_swapULE64(value);
}

PhysFS::sint16
PhysFS::Util::swapSBE16(sint16 value) noexcept
{
	return PHYSFS_swapSBE16(value);
}

PhysFS::uint16
PhysFS::Util::swapUBE16(uint16 value) noexcept
{
	return PHYSFS_swapUBE16(value);
}

PhysFS::sint32
PhysFS::Util::swapSBE32(sint32 value) noexcept
{
	return PHYSFS_swapSBE32(value);
}

PhysFS::uint32
PhysFS::Util::swapUBE32(uint32 value) noexcept
{
	return PHYSFS_swapUBE32(value);
}

PhysFS::sint64
PhysFS::Util::swapSBE64(sint64 value) noexcept
{
	return PHYSFS_swapSBE64(value);
}

PhysFS::uint64
PhysFS::Util::swapUBE64(uint64 value) noexcept
{
	return PHYSFS_swapUBE64(value);
}

std::string
PhysFS::Util::utf8FromUcs4(const uint32* src)
{
	std::string value;
	const std::size_t length = strlen(reinterpret_cast<const char*>(src));
	char* buffer = new char[length]; // will be smaller than len
	PHYSFS_utf8FromUcs4(src, buffer, length);
	value.append(buffer);
	return value;
}

std::string
PhysFS::Util::utf8ToUcs4(const char* src)
{
	std::string value;
	const std::size_t length = strlen(src) * 4;
	char* buffer = new char[length]; // will be smaller than len
	PHYSFS_utf8ToUcs4(src, reinterpret_cast<uint32*>(buffer), length);
	value.append(buffer);
	return value;
}

std::string
PhysFS::Util::utf8FromUcs2(const uint16* src)
{
	std::string value;
	const std::size_t length = strlen(reinterpret_cast<const char*>(src));
	char * buffer = new char[length]; // will be smaller than len
	PHYSFS_utf8FromUcs2(src, buffer, length);
	value.append(buffer);
	return value;
}

std::string
PhysFS::Util::utf8ToUcs2(const char* src)
{
	std::string value;
	std::size_t length = strlen(src) * 2;
	char * buffer = new char[length]; // will be smaller than len
	PHYSFS_utf8ToUcs2(src, reinterpret_cast<uint16*>(buffer), length);
	value.append(buffer);
	return value;
}

std::string
PhysFS::Util::utf8FromLatin1(const char* src)
{
	std::string value;
	const std::size_t length = strlen(reinterpret_cast<const char*>(src)) * 2;
	char * buffer = new char[length]; // will be smaller than len
	PHYSFS_utf8FromLatin1(src, buffer, length);
	value.append(buffer);
	return value;
}

