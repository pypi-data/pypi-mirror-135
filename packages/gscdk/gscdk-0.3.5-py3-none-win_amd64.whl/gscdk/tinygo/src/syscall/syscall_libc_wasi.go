// +build wasi eosio

package syscall

// https://github.com/WebAssembly/wasi-libc/blob/main/expected/wasm32-wasi/predefined-macros.txt

type Signal int

const (
	SIGCHLD = 16
	SIGINT  = 2
	SIGKILL = 9
	SIGTRAP = 5
	SIGQUIT = 3
	SIGTERM = 15
)

const (
	Stdin  = 0
	Stdout = 1
	Stderr = 2
)

const (
	__WASI_OFLAGS_CREAT   = 1
	__WASI_FDFLAGS_APPEND = 1
	__WASI_OFLAGS_EXCL    = 4
	__WASI_OFLAGS_TRUNC   = 8
	__WASI_FDFLAGS_SYNC   = 16

	O_RDONLY = 0x04000000
	O_WRONLY = 0x10000000
	O_RDWR   = O_RDONLY | O_WRONLY

	O_CREAT  = __WASI_OFLAGS_CREAT << 12
	O_TRUNC  = __WASI_OFLAGS_TRUNC << 12
	O_APPEND = __WASI_FDFLAGS_APPEND
	O_EXCL   = __WASI_OFLAGS_EXCL << 12
	O_SYNC   = __WASI_FDFLAGS_SYNC

	O_CLOEXEC = 0
)

//go:extern errno
var libcErrno uintptr

func getErrno() error {
	return Errno(libcErrno)
}

func (e Errno) Is(target error) bool {
	switch target.Error() {
	case "permission denied":
		return e == EACCES || e == EPERM || e == ENOTCAPABLE // ENOTCAPABLE is unique in WASI
	case "file already exists":
		return e == EEXIST || e == ENOTEMPTY
	case "file does not exist":
		return e == ENOENT
	}
	return false
}

// https://github.com/WebAssembly/wasi-libc/blob/main/libc-bottom-half/headers/public/__errno.h
const (
	E2BIG           Errno = 1      /* Argument list too long */
	EACCES          Errno = 2      /* Permission denied */
	EADDRINUSE      Errno = 3      /* Address already in use */
	EADDRNOTAVAIL   Errno = 4      /* Address not available */
	EAFNOSUPPORT    Errno = 5      /* Address family not supported by protocol family */
	EAGAIN          Errno = 6      /* Try again */
	EWOULDBLOCK     Errno = EAGAIN /* Operation would block */
	EALREADY        Errno = 7      /* Socket already connected */
	EBADF           Errno = 8      /* Bad file number */
	EBADMSG         Errno = 9      /* Trying to read unreadable message */
	EBUSY           Errno = 10     /* Device or resource busy */
	ECANCELED       Errno = 11     /* Operation canceled. */
	ECHILD          Errno = 12     /* No child processes */
	ECONNABORTED    Errno = 13     /* Connection aborted */
	ECONNREFUSED    Errno = 14     /* Connection refused */
	ECONNRESET      Errno = 15     /* Connection reset by peer */
	EDEADLK         Errno = 16     /* Deadlock condition */
	EDESTADDRREQ    Errno = 17     /* Destination address required */
	EDOM            Errno = 18     /* Math arg out of domain of func */
	EDQUOT          Errno = 19     /* Quota exceeded */
	EEXIST          Errno = 20     /* File exists */
	EFAULT          Errno = 21     /* Bad address */
	EFBIG           Errno = 22     /* File too large */
	EHOSTUNREACH    Errno = 23     /* Host is unreachable */
	EIDRM           Errno = 24     /* Identifier removed */
	EILSEQ          Errno = 25
	EINPROGRESS     Errno = 26 /* Connection already in progress */
	EINTR           Errno = 27 /* Interrupted system call */
	EINVAL          Errno = 28 /* Invalid argument */
	EIO             Errno = 29 /* I/O error */
	EISCONN         Errno = 30 /* Socket is already connected */
	EISDIR          Errno = 31 /* Is a directory */
	ELOOP           Errno = 32 /* Too many symbolic links */
	EMFILE          Errno = 33 /* Too many open files */
	EMLINK          Errno = 34 /* Too many links */
	EMSGSIZE        Errno = 35 /* Message too long */
	EMULTIHOP       Errno = 36 /* Multihop attempted */
	ENAMETOOLONG    Errno = 37 /* File name too long */
	ENETDOWN        Errno = 38 /* Network interface is not configured */
	ENETRESET       Errno = 39
	ENETUNREACH     Errno = 40         /* Network is unreachable */
	ENFILE          Errno = 41         /* File table overflow */
	ENOBUFS         Errno = 42         /* No buffer space available */
	ENODEV          Errno = 43         /* No such device */
	ENOENT          Errno = 44         /* No such file or directory */
	ENOEXEC         Errno = 45         /* Exec format error */
	ENOLCK          Errno = 46         /* No record locks available */
	ENOLINK         Errno = 47         /* The link has been severed */
	ENOMEM          Errno = 48         /* Out of memory */
	ENOMSG          Errno = 49         /* No message of desired type */
	ENOPROTOOPT     Errno = 50         /* Protocol not available */
	ENOSPC          Errno = 51         /* No space left on device */
	ENOSYS          Errno = 52         /* Function not implemented */
	ENOTCONN        Errno = 53         /* Socket is not connected */
	ENOTDIR         Errno = 54         /* Not a directory */
	ENOTEMPTY       Errno = 55         /* Directory not empty */
	ENOTSOCK        Errno = 57         /* Socket operation on non-socket */
	ESOCKTNOSUPPORT Errno = 58         /* Socket type not supported */
	EOPNOTSUPP      Errno = 58         /* Operation not supported on transport endpoint */
	ENOTSUP         Errno = EOPNOTSUPP /* Not supported */
	ENOTTY          Errno = 59         /* Not a typewriter */
	ENXIO           Errno = 60         /* No such device or address */
	EOVERFLOW       Errno = 61         /* Value too large for defined data type */
	EPERM           Errno = 63         /* Operation not permitted */
	EPIPE           Errno = 64         /* Broken pipe */
	EPROTO          Errno = 65         /* Protocol error */
	EPROTONOSUPPORT Errno = 66         /* Unknown protocol */
	EPROTOTYPE      Errno = 67         /* Protocol wrong type for socket */
	ERANGE          Errno = 68         /* Math result not representable */
	EROFS           Errno = 69         /* Read-only file system */
	ESPIPE          Errno = 70         /* Illegal seek */
	ESRCH           Errno = 71         /* No such process */
	ESTALE          Errno = 72
	ETIMEDOUT       Errno = 73 /* Connection timed out */
	EXDEV           Errno = 75 /* Cross-device link */
	ENOTCAPABLE     Errno = 76 /* Extension: Capabilities insufficient. */
)
