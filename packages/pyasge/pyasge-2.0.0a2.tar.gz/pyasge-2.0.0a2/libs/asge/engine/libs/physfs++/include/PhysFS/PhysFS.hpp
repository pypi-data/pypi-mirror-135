#pragma once
#ifdef PHYSFS_CPP_STATIC
    #define PHYSFS_LIB_API
#elif _WIN32 || defined __CYGWIN__ || defined __MINGW32__
    #ifdef PHYSFS_EXPORT_LIB
        #define PHYSFS_LIB_API __declspec(dllexport)
    #else
        #define PHYSFS_LIB_API __declspec(dllimport)
    #endif
#else
  #if __GNUC__ >= 4
    #define PHYSFS_LIB_API __attribute__ ((visibility ("default")))
  #else
    #define PHYSFS_LIB_API
  #endif
#endif

#include <string>
#include <vector>
#include <physfs.h>

/**
*  PhysFS++.
*  PhysFS++ is a C++ wrapper for the PhysFS library. It exposes
*  the libraries original functionality through the PhysFS
*  namespace. These functions are simple and generally only 
*  proxy the call to the original C library. The function names
*  have been retained so the PhysFS original documentation is 
*  valid and should be used to explore the pseudo-fs functionality.
*  Most of the changes are the use of std:string instead of a basic
*  c string. This library was inspired by https://github.com/kahowell/physfs-cpp
*  @see PhysFS
*  @see https://icculus.org/physfs/
*/
namespace PhysFS
{
	enum IOResult
	{
		PHYSFS_ERROR = 0,
		PHYSFS_OK = 1
	};

	enum class IOMode
	{
		READ,
		APPEND,
		WRITE
	};

	using FileType = PHYSFS_FileType;
	using FileIO_ErrorCode = PHYSFS_ErrorCode;
	using StringList = std::vector<std::string>;

	using uint8 = PHYSFS_uint8;
	using sint8 = PHYSFS_sint8;
	using uint16 = PHYSFS_uint16;
	using sint16 = PHYSFS_sint16;
	using uint32 = PHYSFS_uint32;
	using sint32 = PHYSFS_sint32;
	using uint64 = PHYSFS_uint64;
	using sint64 = PHYSFS_sint64;

	using MetaData = PHYSFS_Stat;
	using StringCallback = PHYSFS_StringCallback;
	using EnumFilesCallback = PHYSFS_EnumerateCallback;
	using Version = PHYSFS_Version;
	using Allocator = PHYSFS_Allocator;
	using ArchiveInfo = PHYSFS_ArchiveInfo;
	using ArchiveInfoList = std::vector<ArchiveInfo>;

	PHYSFS_LIB_API IOResult init(char const * argv0) noexcept;
	PHYSFS_LIB_API IOResult deinit() noexcept;
	PHYSFS_LIB_API PHYSFS_File* open(const std::string& file_name, IOMode mode);
	PHYSFS_LIB_API bool close(PHYSFS_File* file) noexcept;
	PHYSFS_LIB_API sint64 writeBytes(PHYSFS_File *handle, const void *buffer, uint64 length);
	PHYSFS_LIB_API sint64 readBytes(PHYSFS_File *handle, void *buffer, uint64 length);
	PHYSFS_LIB_API sint64 length( PHYSFS_File* handle);
	PHYSFS_LIB_API int seek(PHYSFS_file* handle, uint64 pos);
    PHYSFS_LIB_API void setSaneConfig(const std::string& org_name, const std::string& game_name, const std::string& archiveExt, bool includeCdRoms, bool archivesFirst) noexcept;
	PHYSFS_LIB_API IOResult mount(const std::string& dir, const std::string& mount_point, bool append_to_path) noexcept;
	PHYSFS_LIB_API void unmount(const std::string& old_dir) noexcept;
	PHYSFS_LIB_API ArchiveInfoList supportedArchiveTypes();
	PHYSFS_LIB_API StringList getCdRomDirs();
	PHYSFS_LIB_API void getCdRomDirs(StringCallback callback, void* extra) noexcept;
	PHYSFS_LIB_API StringList getSearchPath();
	PHYSFS_LIB_API void getSearchPath(StringCallback callback, void* data) noexcept;
	PHYSFS_LIB_API Version getLinkedVersion() noexcept;
	PHYSFS_LIB_API std::string getDirSeparator();
	PHYSFS_LIB_API void permitSymbolicLinks(bool allow) noexcept;
	PHYSFS_LIB_API std::string getBaseDir();
	PHYSFS_LIB_API std::string getPrefDir(const std::string& org_name, const std::string& app_name);
	PHYSFS_LIB_API std::string getWriteDir();
	PHYSFS_LIB_API IOResult setWriteDir(const std::string& new_dir) noexcept;
	PHYSFS_LIB_API int mkdir(const std::string& dir_name) noexcept;
	PHYSFS_LIB_API int deleteFile(const std::string& filename) noexcept;
	PHYSFS_LIB_API std::string getRealDir(const std::string& filename);
	PHYSFS_LIB_API StringList enumerateFiles(const std::string& directory) noexcept;
	PHYSFS_LIB_API void enumerateFiles(const std::string& directory, EnumFilesCallback callback, void* data) noexcept;
	PHYSFS_LIB_API bool exists(const std::string& filename) noexcept;
	PHYSFS_LIB_API bool isDirectory(const std::string& filename) noexcept;
	PHYSFS_LIB_API MetaData getMetaData(const std::string& meta) noexcept;
	PHYSFS_LIB_API bool isSymbolicLink(const std::string& filename) noexcept;
	PHYSFS_LIB_API sint64 getLastModTime(const std::string& filename) noexcept;
	PHYSFS_LIB_API bool isInititalised() noexcept;
	PHYSFS_LIB_API bool symbolicLinksPermitted() noexcept;
	PHYSFS_LIB_API IOResult setAllocator(Allocator const * allocator) noexcept;
	PHYSFS_LIB_API FileIO_ErrorCode getLastErrorCode() noexcept;
	PHYSFS_LIB_API std::string getMountPoint(const std::string& dir);


	/**
	* Util.
	* Utility functions for swapping endianness and managing UTF
	* strings. They simply proxy calls to the underlying PhysFS 
	* library. They have been wrapped inside their own nested namespace 
	* to create a better level of seperation.
	*/
	namespace Util {
		PHYSFS_LIB_API sint16 swapSLE16(sint16 value) noexcept;
		PHYSFS_LIB_API uint16 swapULE16(uint16 value) noexcept;
		PHYSFS_LIB_API sint32 swapSLE32(sint32 value) noexcept;
		PHYSFS_LIB_API uint32 swapULE32(uint32 value) noexcept;
		PHYSFS_LIB_API sint64 swapSLE64(sint64 value) noexcept;
		PHYSFS_LIB_API uint64 swapULE64(uint64 value) noexcept;
		PHYSFS_LIB_API sint16 swapSBE16(sint16 value) noexcept;
		PHYSFS_LIB_API uint16 swapUBE16(uint16 value) noexcept;
		PHYSFS_LIB_API sint32 swapSBE32(sint32 value) noexcept;
		PHYSFS_LIB_API uint32 swapUBE32(uint32 value) noexcept;
		PHYSFS_LIB_API sint64 swapSBE64(sint64 value) noexcept;
		PHYSFS_LIB_API uint64 swapUBE64(uint64 value) noexcept;

		PHYSFS_LIB_API std::string utf8FromUcs4(uint32 const * src);
		PHYSFS_LIB_API std::string utf8ToUcs4(char const * src);
		PHYSFS_LIB_API std::string utf8FromUcs2(uint16 const * src);
		PHYSFS_LIB_API std::string utf8ToUcs2(char const * src);
		PHYSFS_LIB_API std::string utf8FromLatin1(char const * src);
	}
}