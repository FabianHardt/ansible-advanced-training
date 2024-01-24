package utils;

/**
 * This class contains utility functions for generating useless data.
 */
public class UselessDataGenerator {

    /**
     * Generates useless data.
     *
     * @param size The size of the useless data to generate.
     * @return Returns an array of useless data.
     */
    public static int[] generateUselessData(int size) {
        int[] data = new int[size];
        for (int i = 0; i < size; i++) {
            data[i] = i;
        }
        return data;
    }

    /**
     * Prints the useless data.
     *
     * @param data The useless data to print.
     */
    public static void printUselessData(int[] data) {
        for (int i = 0; i < data.length; i++) {
            System.out.println(data[i]);
        }
    }

    /**
     * Main method to demonstrate the usage of the UselessDataGenerator class.
     *
     * @param args The command line arguments.
     */
    public static void main(String[] args) {
        int[] uselessData = generateUselessData(10);
        printUselessData(uselessData);
    }
}
