import { View, Text, Animated } from 'react-native'
import React, { useEffect, useState } from 'react'

const BlinkDot = ({ duration, children } : { duration: number, children: any}) => {
  const [fadeAnimation, setfadeAnimation] = useState(new Animated.Value(0.5))

  useEffect(() => {
    Animated.loop(
        Animated.sequence([
            Animated.timing(fadeAnimation, {
                toValue: 1,
                duration: duration,
                useNativeDriver: true
            })
        ])
    ).start()
  })

  return (
    <View>
      <Animated.View style={{ opacity: fadeAnimation }}>{children}</Animated.View>
    </View>
  )
}

export default BlinkDot