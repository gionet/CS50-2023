SELECT title, rating
FROM movies
JOIN ratings ON movie_id = movies.id
WHERE year = 2010
GROUP BY title
ORDER BY rating DESC;