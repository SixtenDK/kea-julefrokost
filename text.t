    <!-- Julefrokost tilmelding -->
    <style>
        form {
            display: flex;
            flex-direction: column;
            width: 200px;
        }

        label {
            margin-bottom: 5px;
        }

        input {
            margin-bottom: 10px;
        }
    </style>

    <h1>Julefrokost tilmelding</h1>
    <form action="index.php" method="post">
        <label for="name">Navn:</label>
        <input type="text" name="name" id="name" required>
        <br>
        <label for="email">Email:</label>
        <input type="email" name="email" id="email" required>
        <br>
        <label for="phone">Telefon:</label>
        <input type="tel" name="phone" id="phone" required>
        <br>
        <label for="payment">Betalings mulighed:</label>
        <select name="payment" id="payment">
            <option value="mobilepay">MobilePay</option>
            <option value="cash">Cash</option>
        </select>
        <br>
        <input type="submit" value="Tilmeld">
    </form>

    <!-- Deltagere -->
    <h2>Deltagere</h2>
    {% for participant in participants %}
        <p>{{ participant }}</p>
    {% endfor %}