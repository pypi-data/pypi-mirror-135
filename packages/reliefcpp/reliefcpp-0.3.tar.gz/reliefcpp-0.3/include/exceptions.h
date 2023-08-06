#ifndef EXCEPTIONS_H
#define EXCEPTIONS_H

#include <exception>

class Exception : public std::exception {
public:
    Exception(const char* str)
    {
        this->str = str;
    }

    virtual const char* what() const throw()
    {
        return this->str;
    }

private:
    const char* str;
};

#endif