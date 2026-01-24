import { getRestaurants } from "./services/dining.service.js";
import { getCoordinates } from "./services/places.service.js";
import "dotenv/config";

async function test() {
    const destination = "Paris";
    console.log(`Testing dining for ${destination}...`);

    const coords = await getCoordinates(destination);
    if (!coords) {
        console.error("Could not get coordinates");
        return;
    }
    console.log("Coordinates:", coords);

    const restaurants = await getRestaurants(coords.lat, coords.lon);
    console.log("Restaurants found:", restaurants.length);
    console.log(restaurants.slice(0, 3));
}

test();
