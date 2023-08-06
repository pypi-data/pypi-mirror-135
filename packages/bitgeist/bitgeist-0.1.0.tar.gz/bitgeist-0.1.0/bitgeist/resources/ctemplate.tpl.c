#include "geisten.h"
#include <stdlib.h>
#include <stdio.h>
#include <err.h>

//define the weights and parameters

$declaration

int main(int argc, const char *argv[argc]) {
    //open a file to read the input data (remember: everything is a file!)

    FILE *in_file = fopen("name_of_file", "r"); // read only

    if (!in_file) {
        err(EXIT_FAILED, "reading file");
    }

    // attempt to read the array of type $input_type and store 
    // the value in the "input" array 
    while (fread($input_name, sizeof($input_type), $input_size, in_file) == $input_size) {
        $layers
        printf("%d\n", $output_value[0]);
    }
    return EXIT_SUCCESS;
}