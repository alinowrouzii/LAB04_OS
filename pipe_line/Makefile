CC      = gcc
CFLAGS  = -g
RM      = rm -f


default: all

all: User_one User_two

User_one: user_one.c
	$(CC) $(CFLAGS) -o user_one user_one.c

User_two: user_two.c
	$(CC) $(CFLAGS) -o user_two user_two.c

clean veryclean:
	$(RM) user_one user_two