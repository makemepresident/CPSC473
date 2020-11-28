import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Scanner;

public class Driver {

    public static void main(String[] args) {

        String filepath = System.getProperty("user.dir") + "\\Datasets" + "\\" + args[0];
        FPGrowth fp = new FPGrowth(filepath, 0.5, 10);
    }
}

class FPGrowth {

    HashMap<Integer, Link> header_table;
    int db_length;
    double minsup;
    int max_value;

    FPGrowth(String filepath, double minsup, int max_value) {
        this.max_value = max_value;
        this.minsup = minsup;
        this.header_table = gen_header_table(filepath);
        // gen_tree(filepath);
    }

    // void gen_tree(String filepath) {
    //     File input = new File(filepath);
    //     // ArrayList<Link> unique = new ArrayList<Link>();
    //     Link[] unique = new Link[this.max_value];
    //     Node root = new Node(0);
    //     try {
    //         Scanner reader = new Scanner(input);
    //         boolean first = true;
    //         while(reader.hasNextLine()) {
    //             if(first) {
    //                 first = false;
    //                 continue;
    //             }
    //             int[] elements = parseElements(reader.nextLine());

    //         }
    //     } catch(FileNotFoundException e) {
    //         //TODO: fix
    //     }
    // }

    HashMap<Integer, Link> gen_header_table(String filepath) {
        File input = new File(filepath);
        HashMap<Integer, Link> header_table = new HashMap<Integer, Link>();
        try {
            Scanner reader = new Scanner(input);
            boolean first = true;
            while(reader.hasNextLine()) {
                if(first) {
                    this.db_length = Integer.parseInt(reader.nextLine());
                    first = false;
                    continue;
                }
                int[] elements = parseElements(reader.nextLine());
                for(int i : elements) {
                    if(!header_table.containsKey(i)) {
                        header_table.put(i, new Link(i));
                    } else {
                        header_table.get(i).count++;
                    }
                }
            }
            reader.close();
        } catch(FileNotFoundException e) {
            // TODO: ODODODODO
        }
        return header_table;
    }

    // Link[] gen_header_table(String filepath) {
    //     File input = new File(filepath);
    //     // ArrayList<Link> unique = new ArrayList<Link>();
    //     Link[] unique = new Link[this.max_value];
    //     try {
    //         Scanner reader = new Scanner(input);
    //         boolean first = true;
    //         while(reader.hasNextLine()) {
    //             if(first) {
    //                 this.db_length = Integer.parseInt(reader.nextLine());
    //                 first = false;
    //                 continue;
    //             }
    //             int[] elements = parseElements(reader.nextLine()); // [2, 3, 5]
    //             for(int i : elements) {
    //                 Link ins = new Link(i);
    //                 if(unique[i] == null) {
    //                     unique[i] = ins;
    //                 } else {
    //                     unique[i].count++;
    //                 }
    //                 // if(!unique.contains(ins)) {
    //                 //     unique.add(new Link(i));
    //                 // } else {
    //                 //     unique.get(i).count++;
    //                 // }
    //             }
    //         }
    //         this.header_table = prune_sort(unique);
    //         // unique.trimToSize();
    //         reader.close();
    //     } catch(FileNotFoundException e) {
    //         System.out.println(e);
    //         //TODO: handle exception
    //     }
    //     return unique;
    // }

    int[] parseElements(String line) {
        String elements = line.split("\t")[2];
        int[] arr = Arrays.stream(elements.split(" |\n")).mapToInt(Integer::parseInt).toArray();
        return arr;
    }

    ArrayList<Link> prune_sort(Link[] arr) {
        ArrayList<Link> header_table = new ArrayList<Link>();
        for(Link i : arr) {
            if(i == null)
                continue;
            header_table.add(i);
        }
        Collections.sort(header_table);
        for(Iterator<Link> it = header_table.iterator(); it.hasNext();) {
            Link i = it.next();
            if(i.count < this.db_length * this.minsup)
                it.remove();
        }
        return header_table;
    }
}

class Node {

    int value;
    int count;
    HashMap<Integer, Node> children;

    Node(int value) {
        this.value = value;
        this.count = 1;
        this.children = new HashMap<Integer, Node>();
    }
}

class Link implements Comparable<Link> {

    int value;
    int count;
    ArrayList<Link> pointers;

    Link(int value) {
        this.value = value;
        this.count = 1;
        this.pointers = new ArrayList<Link>();
    }

    public boolean equals(Object v) {
        if(v instanceof Link) {
            Link cp = (Link) v;
            if(cp.value == this.value)
                return true;
        }
        return false;
    }

    @Override
    public int hashCode() {
        // TODO Auto-generated method stub
        return super.hashCode();
    }

    @Override
    public int compareTo(Link cp) {
        return cp.count - this.count;
    }
}