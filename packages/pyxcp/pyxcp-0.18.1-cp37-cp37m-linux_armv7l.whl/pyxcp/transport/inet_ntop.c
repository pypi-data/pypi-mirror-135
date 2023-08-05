#include <stddef.h> // ****
#include <string.h>
#include <stdint.h>
#include <stdio.h>



#include <sys/types.h> // ****
#include <sys/socket.h> // ****
#include <arpa/inet.h>


size_t _strlcpy(char * __restrict dst, const char * __restrict src, size_t siz)
{
	char *d = dst;
	const char *s = src;
	size_t n = siz;

	/* Copy as many bytes as will fit */
	if (n != 0) {
		while (--n != 0) {
			if ((*d++ = *s++) == '\0')
				break;
		}
	}

	/* Not enough room in dst, add NUL and traverse rest of src */
	if (n == 0) {
		if (siz != 0)
			*d = '\0';		/* NUL-terminate dst */
		while (*s++)
			;
	}

	return(s - src - 1);	/* count does not include NUL */
}



char * _inet_ntop(int af, const void *src, char *dst, socklen_t size);

/*%
 * WARNING: Don't even consider trying to compile this on a system where
 * sizeof(int) < 4.  sizeof(int) > 4 is fine; all the world's not a VAX.
 */

static char	*inet_ntop4(const uint8_t *src, char *dst, socklen_t size);
static char	*inet_ntop6(const uint8_t *src, char *dst, socklen_t size);

char * _inet_ntop(int af, const void *src, char *dst, socklen_t size)
{
	switch (af) {
	case AF_INET:
		return (inet_ntop4( (unsigned char*)src, (char*)dst, size)); // ****
	case AF_INET6:
		return (char*)(inet_ntop6( (unsigned char*)src, (char*)dst, size)); // ****
	default:
		// return (NULL); // ****
        return 0 ; // ****
	}
	/* NOTREACHED */
}

static char * inet_ntop4(const uint8_t *src, char *dst, socklen_t size)
{
	static const char fmt[128] = "%u.%u.%u.%u";
	char tmp[sizeof "255.255.255.255"];
	int l;

	// l = snprintf(tmp, sizeof(tmp), fmt, src[0], src[1], src[2], src[3]); // ****
    l = sprintf( tmp, fmt, src[0], src[1], src[2], src[3] ); // **** vc++ does not have snprintf
	if (l <= 0 || (socklen_t) l >= size) {
		return (NULL);
	}
	_strlcpy(dst, tmp, size);
	return (dst);
}

static char * inet_ntop6(const uint8_t *src, char *dst, socklen_t size)
{
	/*
	 * Note that int32_t and int16_t need only be "at least" large enough
	 * to contain a value of the specified size.  On some systems, like
	 * Crays, there is no such thing as an integer variable with 16 bits.
	 * Keep this in mind if you think this function should have been coded
	 * to use pointer overlays.  All the world's not a VAX.
	 */
	char tmp[sizeof "ffff:ffff:ffff:ffff:ffff:ffff:255.255.255.255"], *tp;
	struct { int base, len; } best, cur;
#define NS_IN6ADDRSZ	16
#define NS_INT16SZ	2
	uint32_t words[NS_IN6ADDRSZ / NS_INT16SZ];
	int i;

	/*
	 * Preprocess:
	 *	Copy the input (bytewise) array into a wordwise array.
	 *	Find the longest run of 0x00's in src[] for :: shorthanding.
	 */
	memset(words, '\0', sizeof words);
	for (i = 0; i < NS_IN6ADDRSZ; i++) {
		words[i / 2] |= (src[i] << ((1 - (i % 2)) << 3));
    }
	best.base = -1;
	best.len = 0;
	cur.base = -1;
	cur.len = 0;
	for (i = 0; i < (NS_IN6ADDRSZ / NS_INT16SZ); i++) {
		if (words[i] == 0) {
			if (cur.base == -1)
				cur.base = i, cur.len = 1;
			else
				cur.len++;
		} else {
			if (cur.base != -1) {
				if (best.base == -1 || cur.len > best.len)
					best = cur;
				cur.base = -1;
			}
		}
	}
	if (cur.base != -1) {
		if (best.base == -1 || cur.len > best.len)
			best = cur;
	}
	if (best.base != -1 && best.len < 2)
		best.base = -1;

	/*
	 * Format the result.
	 */
	tp = tmp;
	for (i = 0; i < (NS_IN6ADDRSZ / NS_INT16SZ); i++) {
		/* Are we inside the best run of 0x00's? */
		if (best.base != -1 && i >= best.base &&
		    i < (best.base + best.len)) {
			if (i == best.base)
				*tp++ = ':';
			continue;
		}
		/* Are we following an initial run of 0x00s or any real hex? */
		if (i != 0)
			*tp++ = ':';
		/* Is this address an encapsulated IPv4? */
		if (i == 6 && best.base == 0 && (best.len == 6 ||
		    (best.len == 7 && words[7] != 0x0001) ||
		    (best.len == 5 && words[5] == 0xffff))) {
			if (!inet_ntop4(src+12, tp, sizeof tmp - (tp - tmp)))
				return (NULL);
			tp += strlen(tp);
			break;
		}
		tp += sprintf(tp, "%x", words[i]); // ****
	}
	/* Was it a trailing run of 0x00's? */
	if (best.base != -1 && (best.base + best.len) ==
	    (NS_IN6ADDRSZ / NS_INT16SZ))
		*tp++ = ':';
	*tp++ = '\0';

	/*
	 * Check for overflow, copy, and we're done.
	 */
	if ((socklen_t)(tp - tmp) > size) {
		return (NULL);
	}
	strcpy(dst, tmp);
	return (dst);
}

/*! \file */


int main()
{
    struct in_addr ipv4_address ;
    struct in6_addr ipv6_address ;
    char cstr[INET_ADDRSTRLEN];
    char * ptr;

    ipv6_address.__in6_u.__u6_addr32[0] = 0x1111;
    ipv6_address.__in6_u.__u6_addr32[1] = 0x2222;
    ipv6_address.__in6_u.__u6_addr32[2] = 0x3333;
    ipv6_address.__in6_u.__u6_addr32[3] = 0x4444;

    ptr = _inet_ntop( AF_INET6, &ipv6_address, cstr, INET_ADDRSTRLEN );
    printf("%s %s\n", cstr, ptr);
//    std::cout << std::hex << std::showbase << ipv4_address.s_addr << '\n'    << std::bitset<32>(ipv4_address.s_addr) << '\n' ;
}

