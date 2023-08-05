/*
 * Copyright (C) 1996-2021  Internet Software Consortium.
 *
 * Permission to use, copy, modify, and distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.
 *
 * THE SOFTWARE IS PROVIDED "AS IS" AND INTERNET SOFTWARE CONSORTIUM
 * DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
 * INTERNET SOFTWARE CONSORTIUM BE LIABLE FOR ANY SPECIAL, DIRECT,
 * INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
 * FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
 * NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
 * WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 */
/*
 * Original code by Paul Vixie. "curlified" by Gisle Vanem.
 */


#include <sys/param.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#include <errno.h>

#define IN6ADDRSZ       16
#define INADDRSZ         4
#define INT16SZ          2

/*
 * Format an IPv4 address, more or less like inet_ntop().
 *
 * Returns `dst' (as a const)
 * Note:
 *  - uses no statics
 *  - takes a unsigned char* not an in_addr as input
 */
static char *inet_ntop4 (const unsigned char *src, char *dst, size_t size)
{
  char tmp[sizeof("255.255.255.255")];
  size_t len;

  tmp[0] = '\0';
  (void)sprintf(tmp, "%d.%d.%d.%d",
                  ((int)((unsigned char)src[0])) & 0xff,
                  ((int)((unsigned char)src[1])) & 0xff,
                  ((int)((unsigned char)src[2])) & 0xff,
                  ((int)((unsigned char)src[3])) & 0xff);

  len = strlen(tmp);
  if(len == 0 || len >= size) {
    errno = ENOSPC;
    return (NULL);
  }
  strcpy(dst, tmp);
  return dst;
}

/*
 * Convert IPv6 binary address into presentation (printable) format.
 */
static char *inet_ntop6 (const unsigned char *src, char *dst, size_t size)
{
  char tmp[sizeof("ffff:ffff:ffff:ffff:ffff:ffff:255.255.255.255")];
  char *tp;
  struct {
    long base;
    long len;
  } best, cur;
  unsigned long words[IN6ADDRSZ / INT16SZ];
  int i;

  /* Preprocess:
   *  Copy the input (bytewise) array into a wordwise array.
   *  Find the longest run of 0x00's in src[] for :: shorthanding.
   */
  memset(words, '\0', sizeof(words));
  for(i = 0; i < IN6ADDRSZ; i++)
    words[i/2] |= (src[i] << ((1 - (i % 2)) << 3));

  best.base = -1;
  cur.base  = -1;
  best.len = 0;
  cur.len = 0;

  for(i = 0; i < (IN6ADDRSZ / INT16SZ); i++) {
    if(words[i] == 0) {
      if(cur.base == -1)
        cur.base = i, cur.len = 1;
      else
        cur.len++;
    }
    else if(cur.base != -1) {
      if(best.base == -1 || cur.len > best.len)
        best = cur;
      cur.base = -1;
    }
  }
  if((cur.base != -1) && (best.base == -1 || cur.len > best.len))
    best = cur;
  if(best.base != -1 && best.len < 2)
    best.base = -1;
  /* Format the result. */
  tp = tmp;
  for(i = 0; i < (IN6ADDRSZ / INT16SZ); i++) {
    /* Are we inside the best run of 0x00's? */
    if(best.base != -1 && i >= best.base && i < (best.base + best.len)) {
      if(i == best.base)
        *tp++ = ':';
      continue;
    }

    /* Are we following an initial run of 0x00s or any real hex?
     */
    if(i)
      *tp++ = ':';

    /* Is this address an encapsulated IPv4?
     */
    if(i == 6 && best.base == 0 &&
        (best.len == 6 || (best.len == 5 && words[5] == 0xffff))) {
      if(!inet_ntop4(src + 12, tp, sizeof(tmp) - (tp - tmp))) {
        errno = ENOSPC;
        return (NULL);
      }
      tp += strlen(tp);
      break;
    }
    tp += sprintf(tp, "%lx", words[i]);
  }

  /* Was it a trailing run of 0x00's?
   */
  if(best.base != -1 && (best.base + best.len) == (IN6ADDRSZ / INT16SZ))
     *tp++ = ':';
  *tp++ = '\0';

  /* Check for overflow, copy, and we're done.
   */
  if((size_t)(tp - tmp) > size) {
    errno = ENOSPC;
    return (NULL);
  }
  strcpy(dst, tmp);
  return dst;
}

char *Curl_inet_ntop(int af, const void *src, char *buf, size_t size)
{
  switch(af) {
  case AF_INET:
    return inet_ntop4((const unsigned char *)src, buf, size);
  case AF_INET6:
    return inet_ntop6((const unsigned char *)src, buf, size);
  default:
    errno = EAFNOSUPPORT;
    return NULL;
  }
}

int main()
{
    struct in_addr ipv4_address ;
    struct in6_addr ipv6_address ;
    char cstr[96];
    char * ptr;

    //ipv6_address.__in6_u.__u6_addr32[0] = 0x1111;
    ipv6_address.__in6_u.__u6_addr32[0] = 0x0000;
    //ipv6_address.__in6_u.__u6_addr32[1] = 0x2222;
    ipv6_address.__in6_u.__u6_addr32[1] = 0x0000;
    ipv6_address.__in6_u.__u6_addr32[2] = 0x3333;
    ipv6_address.__in6_u.__u6_addr32[3] = 0x4444;

    ptr = Curl_inet_ntop( AF_INET6, &ipv6_address, cstr, 96);
    printf("%s\n", cstr);

    ptr = Curl_inet_ntop( AF_INET, &ipv4_address, cstr, 96);
    printf("%s\n", cstr);
}

