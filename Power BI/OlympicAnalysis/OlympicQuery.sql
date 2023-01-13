SELECT 
		[ID]
		,[Name] AS 'Competitor Name'
		,CASE WHEN Sex = 'M' THEN 'Male' ELSE 'Female' END AS Sex	-- Use more descriptive names than M and F
		,[Age]
		,CASE	WHEN [Age] < 18 THEN 'Under 18'						-- Case statement to put Age into different buckets
				WHEN [Age] BETWEEN 18 AND 25 THEN '18-25'
				WHEN [Age] BETWEEN 25 AND 30 THEN '25-30'
				WHEN [Age] > 30 THEN 'Over 30'
		END AS [Age Grouping]
		,[Height]
		,[WEIGHT]
		,[NOC] AS 'Nation Code'
		,LEFT(Games, CHARINDEX(' ', Games)-1) AS 'Year'					-- Isolate Year
		,RIGHT(Games, CHARINDEX(' ', REVERSE(Games))-1) AS 'Season'		-- Isolate Season
		,[Sport]
		,[Event]
		,CASE WHEN Medal = 'NA' THEN 'Not Registered' ELSE Medal END AS Medal	-- Change NA to Not Registered
FROM [Olympic Data].dbo.athletes_event_results
WHERE RIGHT(Games, CHARINDEX(' ', REVERSE(Games))-1) = 'Summer'		-- Isolate Summer Games