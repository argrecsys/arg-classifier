/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package es.uam.irg.utils;

import es.uam.irg.io.IOManager;
import es.uam.irg.nlp.am.Constants;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

/**
 *
 * @author ansegura
 */
public class FunctionUtils {
    
    /**
     *
     * @param <T>
     * @param array
     * @param delimiter
     * @return
     */
    public static <T> String arrayToString(T[] array, String delimiter) {
        String result = "";
        
        if (array != null && array.length > 0) {
            StringBuilder sb = new StringBuilder();
            
            for (T item : array) {
                sb.append(item.toString()).append(delimiter);
            }
            
            result = sb.deleteCharAt(sb.length() - 1).toString();
        }
        
        return result;
    }
    
    /**
     *
     * @param array
     * @return
     */
    public static List<String> createListFromText(String array) {
        array = array.replace("[", "").replace("]", "");
        return new ArrayList<>(Arrays.asList(array.split(",")));
    }
    
    /**
     * 
     * @param dbType
     * @return 
     */
    public static Map<String, Object> getDatabaseConfiguration(String dbType) {
        Map<String, Object> setup = null;
        
        if (dbType.equals(Constants.MYSQL_DB)) {
            setup = IOManager.readYamlFile(Constants.MSQL_SETUP_FILEPATH);
        }
        else if (dbType.equals(Constants.MONGO_DB)) {
            setup = IOManager.readYamlFile(Constants.MDB_SETUP_FILEPATH);
        }
        
        return setup;
    }
    
    /**
     *
     * @param <T>
     * @param array
     * @param startIx
     * @param endIndex
     * @return
     * @throws java.lang.Exception
     */
    public static <T> T[] getSubArray(T[] array, int startIx, int endIndex) throws Exception {
        T[] newArray = null;
        
        if (startIx >= 0 && endIndex <= array.length) {
            newArray = Arrays.copyOfRange(array, startIx, endIndex);
        }
        
        return newArray;
    }
    
    
    /**
     * 
     * @param <T>
     * @param map
     * @return 
     */
    public static <T> List<T> listFromMapKeys(Map<T, ?> map) {
        List<T> list = new ArrayList<>(map.keySet());
        return list;
    }
    
        /**
     * 
     * @param <T>
     * @param set
     * @return 
     */
    public static <T> List<T> listFromSet(Set<T> set) {
        List<T> list = new ArrayList<>();
        list.addAll(set);
        return list;
    }
    
    /**
     *
     * @param list
     * @param sep
     * @return
     */
    public static String listToString(List<String> list, String sep) {
        return list.stream().collect(Collectors.joining(sep+","+sep, sep, sep));
    }
    
    /**
     *
     * @param map
     * @return
     */
    public static Map<String, Integer> sortMapByValue(Map<String, Integer> map) {
        LinkedHashMap<String, Integer> reverseSortedMap = new LinkedHashMap<>();

        //Use Comparator.reverseOrder() for reverse ordering
        map.entrySet()
                .stream()
                .sorted(Map.Entry.comparingByValue(Comparator.reverseOrder()))
                .forEachOrdered(x -> reverseSortedMap.put(x.getKey(), x.getValue()));
        
        return reverseSortedMap;
    }
    
}
