# Izvestaji

## Popularnost žanrova

```sql
SELECT g.title AS genre, COUNT(*) AS count
FROM Book_DW b
JOIN Book_has_Genre_DW bg ON b.idBook = bg.idBook
JOIN Genre_DW g ON bg.idGenre = g.idGenre
GROUP BY g.title
ORDER BY COUNT(*) DESC;
```

## Broj izdatih knjiga po mesecima u 2022. godini

```sql
SELECT
MONTH(startRentDate) AS monthNumber,
    MONTHNAME(startRentDate) AS month,
    COUNT(*) AS booksRentedCount
FROM
    RentedBook_DW
WHERE
    YEAR(startRentDate) = 2022
GROUP BY
    monthNumber, month
ORDER BY
    monthNumber, month;
```

## Broj uplaćenih članarina za svaki kvartal u 2022. godini

```sql
SELECT
    QUARTER(a.startDate) AS quarter,
    COUNT(DISTINCT a.idActiveMembership) AS membershipCount,
    COUNT(DISTINCT r.idRentedBook) AS bookCount
FROM
    ActiveMembership_DW a
    JOIN Time_DW t ON a.Time_DW_idTime_DW = t.idTime_DW
    LEFT JOIN RentedBook_DW r ON t.idTime_DW = r.Time_DW_idTime_DW
WHERE
    YEAR(t.date) = 2022
GROUP BY
    quarter
ORDER BY
    quarter;
```

## Broj aktivnih članova za svaki mesec u tekućoj godini, zaključno sa današnjim datumom

```sql
SELECT
    YEAR(startDate) AS year,
    MONTH(startDate) AS month,
    MONTHNAME(startDate) AS monthName,
    COUNT(*) AS activeMemberCount
FROM
    ActiveMembership_DW
WHERE
    YEAR(startDate) = YEAR(CURDATE()) AND
    startDate <= CURDATE() AND
    expirationDate >= CURDATE()
GROUP BY
    YEAR(startDate),
    MONTH(startDate),
    MONTHNAME(startDate)
ORDER BY
    YEAR(startDate),
    MONTH(startDate);
```

## Broj izdatih knjiga po prodajnim mestima

```sql
SELECT
    bs.idBookStore,
    bs.city,
    COUNT(rb.idRentedBook) AS bookCount
FROM
    BookStore_DW bs
    LEFT JOIN Book_has_BookStore_DW bb ON bs.idBookStore = bb.idBookStore
    LEFT JOIN RentedBook_DW rb ON bb.idBook = rb.idBook AND bb.idBookStore = rb.idBookStore
GROUP BY
    bs.idBookStore,
    bs.city
ORDER BY
    bookCount DESC,
    bs.city;
```

## Prikaz liste top 10 najčitanijih izdavača

```sql
SELECT
    b.publisher,
    COUNT(rb.idRentedBook) AS rentalCount
FROM
    Book_DW b
    JOIN Book_has_BookStore_DW bb ON b.idBook = bb.idBook
    JOIN RentedBook_DW rb ON bb.idBook = rb.idBook AND bb.idBookStore = rb.idBookStore
GROUP BY
    b.publisher
ORDER BY
    rentalCount DESC
LIMIT 10;
```
