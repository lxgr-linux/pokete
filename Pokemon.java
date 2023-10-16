import java.util.Scanner;

class Pokemon {
    String name;
    int health;
    int power;

    public Pokemon(String name, int health, int power) {
        this.name = name;
        this.health = health;
        this.power = power;
    }

    public void attack(Pokemon enemy) {
        enemy.health -= power;
    }

    public boolean isAlive() {
        return health > 0;
    }
}

public class PokemonGame {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        Pokemon playerPokemon = new Pokemon("Pikachu", 100, 20);
        Pokemon enemyPokemon = new Pokemon("Charmander", 100, 15);

        System.out.println("Welcome to the Pokémon Battle!");
        System.out.println("You have " + playerPokemon.name + " with you.");
        System.out.println("A wild " + enemyPokemon.name + " appeared!");

        while (playerPokemon.isAlive() && enemyPokemon.isAlive()) {
            System.out.println("\nYour " + playerPokemon.name + " - Health: " + playerPokemon.health);
            System.out.println("Wild " + enemyPokemon.name + " - Health: " + enemyPokemon.health);

            System.out.print("What will you do? (1. Attack, 2. Run): ");
            int choice = scanner.nextInt();

            if (choice == 1) {
                playerPokemon.attack(enemyPokemon);
                System.out.println("You attacked " + enemyPokemon.name + "!");
            } else if (choice == 2) {
                System.out.println("You ran away from the battle.");
                break;
            } else {
                System.out.println("Invalid choice. Please choose 1 to attack or 2 to run.");
            }

            if (enemyPokemon.isAlive()) {
                enemyPokemon.attack(playerPokemon);
                System.out.println("Wild " + enemyPokemon.name + " attacked you!");
            }
        }

        if (playerPokemon.isAlive()) {
            System.out.println("Congratulations! You defeated wild " + enemyPokemon.name + "!");
        } else {
            System.out.println("You were defeated by wild " + enemyPokemon.name + ". Game Over!");
        }

        scanner.close();
    }
}
