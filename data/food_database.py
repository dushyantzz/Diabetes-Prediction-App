# Food database with nutritional information per 100g
FOOD_DATABASE = {
    'apple': {'carbs': 14, 'calories': 52, 'protein': 0.3, 'fat': 0.2, 'fiber': 2.4, 'gi': 'low'},
    'banana': {'carbs': 23, 'calories': 89, 'protein': 1.1, 'fat': 0.3, 'fiber': 2.6, 'gi': 'medium'},
    'orange': {'carbs': 12, 'calories': 47, 'protein': 0.9, 'fat': 0.1, 'fiber': 2.4, 'gi': 'low'},
    'pizza': {'carbs': 33, 'calories': 266, 'protein': 11, 'fat': 10, 'fiber': 2.5, 'gi': 'high'},
    'burger': {'carbs': 40, 'calories': 354, 'protein': 20, 'fat': 17, 'fiber': 3, 'gi': 'high'},
    'rice': {'carbs': 28, 'calories': 130, 'protein': 2.7, 'fat': 0.3, 'fiber': 0.4, 'gi': 'high'},
    'pasta': {'carbs': 25, 'calories': 131, 'protein': 5, 'fat': 1.1, 'fiber': 1.8, 'gi': 'medium'},
    'bread': {'carbs': 14, 'calories': 74, 'protein': 2.6, 'fat': 1, 'fiber': 1.3, 'gi': 'high'},
    'salad': {'carbs': 3, 'calories': 20, 'protein': 1.2, 'fat': 0.2, 'fiber': 1.8, 'gi': 'low'},
    'chicken': {'carbs': 0, 'calories': 165, 'protein': 31, 'fat': 3.6, 'fiber': 0, 'gi': 'low'},
    'fish': {'carbs': 0, 'calories': 136, 'protein': 22, 'fat': 5, 'fiber': 0, 'gi': 'low'},
    'steak': {'carbs': 0, 'calories': 271, 'protein': 26, 'fat': 19, 'fiber': 0, 'gi': 'low'},
    'broccoli': {'carbs': 6, 'calories': 34, 'protein': 2.8, 'fat': 0.4, 'fiber': 2.6, 'gi': 'low'},
    'carrot': {'carbs': 10, 'calories': 41, 'protein': 0.9, 'fat': 0.2, 'fiber': 2.8, 'gi': 'medium'},
    'potato': {'carbs': 17, 'calories': 77, 'protein': 2, 'fat': 0.1, 'fiber': 2.2, 'gi': 'high'},
    'yogurt': {'carbs': 7, 'calories': 59, 'protein': 3.5, 'fat': 3.3, 'fiber': 0, 'gi': 'low'},
    'cheese': {'carbs': 1.3, 'calories': 402, 'protein': 25, 'fat': 33, 'fiber': 0, 'gi': 'low'},
    'egg': {'carbs': 0.6, 'calories': 155, 'protein': 13, 'fat': 11, 'fiber': 0, 'gi': 'low'},
    'chocolate': {'carbs': 60, 'calories': 546, 'protein': 4.9, 'fat': 31, 'fiber': 7, 'gi': 'medium'},
    'ice cream': {'carbs': 24, 'calories': 207, 'protein': 3.5, 'fat': 11, 'fiber': 0.5, 'gi': 'medium'}
}

# GI level descriptions
GI_DESCRIPTIONS = {
    'low': 'Low glycemic index (55 or less) - Slow carbohydrate absorption, smaller rise in blood glucose levels',
    'medium': 'Medium glycemic index (56-69) - Moderate carbohydrate absorption and blood glucose response',
    'high': 'High glycemic index (70 or more) - Rapid carbohydrate absorption, higher blood glucose spike'
}

# Diabetes management tips based on GI levels
DIABETES_TIPS = {
    'low': "Foods with low GI are generally good choices for people with diabetes as they cause a slower, smaller rise in blood glucose levels.",
    'medium': "Medium GI foods should be consumed in moderation. Consider pairing with protein or healthy fats to reduce the glycemic impact.",
    'high': "High GI foods can cause rapid spikes in blood sugar. Limit portions, combine with low GI foods, or choose lower GI alternatives when possible."
}

# Portion size reference (in grams) for common foods
STANDARD_PORTIONS = {
    'apple': 150,  # Medium apple
    'banana': 120,  # Medium banana
    'orange': 150,  # Medium orange
    'pizza': 100,   # 1 slice
    'burger': 250,  # Standard burger
    'rice': 150,    # 1 cup cooked
    'pasta': 140,   # 1 cup cooked
    'bread': 30,    # 1 slice
    'salad': 150,   # Side salad
    'chicken': 85,  # 3 oz portion
    'fish': 85,     # 3 oz portion
    'steak': 85,    # 3 oz portion
    'broccoli': 90, # 1 cup
    'carrot': 70,   # 1 medium
    'potato': 150,  # 1 medium
    'yogurt': 150,  # 1 container
    'cheese': 30,   # 1 oz
    'egg': 50,      # 1 large egg
    'chocolate': 40, # Small bar
    'ice cream': 65  # 1/2 cup
}
